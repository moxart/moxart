import click
import uuid

from flask import request, render_template
from datetime import datetime
from werkzeug.security import generate_password_hash
from slugify import slugify

from moxart import create_app, db, mail

# BLOCK UTILS
from moxart.utils.token import (
    generate_confirmation_token, confirm_token,
    decrypt_me, encrypt_me
)
from moxart.utils.email import send_me
from moxart.utils.upload import init_client_upload_dir
# END BLOCK UTILS

# BLOCK MODELS
from moxart.models.user import User
from moxart.models.post import Post
from moxart.models.category import Category

# End BLOCK MODELS

app = create_app()
app.app_context().push()


@click.group()
def cli():
    pass


# Initializing Database
@click.command()
def init_db():
    db.create_all()
    click.echo('initialized database')


# Initializing an Admin User
@click.command()
def init_admin():
    admin = User(username=app.config['ADMIN_USERNAME'],
                 email=app.config['ADMIN_EMAIL'],
                 password=app.config['ADMIN_PASSWORD'],
                 admin=True,
                 confirmed=True)

    db.session.add(admin)
    db.session.commit()

    if init_client_upload_dir(app.config['UPLOAD_BASE_PATH'], app.config['UPLOAD_CLIENT_PATH'],
                              app.config['UPLOAD_SUB_DIR'], admin.username):
        click.echo(
            '{} directory has been created successfully'.format(admin.username))

    if send_me(app.config['ADMIN_EMAIL'], 'Email Confirmation', app.config['MAIL_DEFAULT_SENDER'], 'layouts/email/confirm.html', admin.username):
        click.echo('initialized admin user')
    else:
        click.echo('user admin has not been initialized successfully')


# add new admin user
@click.command()
@click.option('-a', '--username', prompt="Username", required=True)
@click.option('-e', '--email', prompt='Email', required=True)
@click.option('-p', '--password', prompt='Password', hide_input=True, confirmation_prompt=True, required=True)
def add_admin(username, email, password):
    if db.session.query(User.username).filter_by(username=username).scalar() is None:
        admin = User(username=username, email=email,
                     password=password, admin=True, confirmed=False)

        db.session.add(admin)
        db.session.commit()

        if init_client_upload_dir(app.config['UPLOAD_BASE_PATH'], app.config['UPLOAD_CLIENT_PATH'],
                                  app.config['UPLOAD_SUB_DIR'], admin.username):
            click.echo(
                '{} directory has been created successfully'.format(admin.username))

        if send_me(email, 'Email Confirmation', app.config['MAIL_DEFAULT_SENDER'], 'layouts/email/confirm.html', username):
            click.echo(
                '{} admin has been created successfully and a verification link has been sent to your email account.'.format(
                    username))
        else:
            click.echo('user admin has not been initialized successfully')
    else:
        click.echo('{} has already been taken'.format(username))


# Initializing a User
@click.command()
@click.option('-u', '--username', prompt='Username', required=True)
@click.option('-e', '--email', prompt='Email', required=True)
@click.option('-p', '--password', prompt='Password', hide_input=True, confirmation_prompt=True, required=True)
def init_user(username, email, password):
    if db.session.query(User.username).filter_by(username=username).scalar() is None:
        user = User(username=username, email=email,
                    password=password, admin=False, confirmed=False)

        db.session.add(user)
        db.session.commit()

        if init_client_upload_dir(app.config['UPLOAD_BASE_PATH'], app.config['UPLOAD_CLIENT_PATH'],
                                  app.config['UPLOAD_SUB_DIR'], user.username):
            click.echo(
                '{} directory has been created successfully'.format(user.username))

        if send_me(email, 'Email Confirmation', app.config['MAIL_DEFAULT_SENDER'], 'layouts/email/confirm.html', username):
            click.echo(
                '{} admin has been created successfully and a verification link has been sent to your email account.'.format(
                    username))
        else:
            click.echo('user has not been initialized successfully')
    else:
        click.echo('The {} has already been taken'.format(username))


# Initializing uncategorized category
@click.command()
def init_category():
    category = Category(category_name="Uncategorized",
                        category_name_slug=slugify("Uncategorized"))

    db.session.add(category)
    db.session.commit()

    click.echo('initialized the uncategorized category')


# add category
@click.command()
@click.option('-c', '--category', prompt="Category Name", required=True)
def add_category(category):
    slug = slugify(category)

    if db.session.query(Category.category_name_slug).filter_by(category_name_slug=slug).scalar() is None:
        cat = Category(category_name=category, category_name_slug=slug)

        db.session.add(cat)
        db.session.commit()

        click.echo('{} category has been created successfully'.format(category))
    else:
        click.echo('The {} has already been taken'.format(category))


# drop category
@click.command()
@click.option('-c', '--category', prompt="Category Name (slug)", required=True)
def drop_category(category):
    if db.session.query(Category.category_name_slug).filter(Category.category_name_slug == category):
        db.session.query(Category.category_name_slug).filter(
            Category.category_name_slug == category).delete()

        db.session.commit()

        click.echo(
            '{} category has been removed successfully from dashboard'.format(category))
    else:
        click.echo('{} category does\'nt exist'.format(category))


# Initializing Hello World Post
@click.command()
def init_post():
    user = User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first()
    category = Category.query.filter_by(
        category_name_slug="uncategorized").first()

    post = Post(user_public_id=user.user_public_id, category_public_id=category.category_public_id,
                title="Hello, World!",
                title_slug="hello-world!",
                content="<p>Cake gummies apple pie liquorice carrot cake caramels biscuit biscuit. "
                        "Cake pastry chocolate icing pudding cheesecake chocolate cake bonbon. "
                        "Chocolate tootsie roll marshmallow jelly-o ice cream. "
                        "Gingerbread fruitcake biscuit jujubes soufflé gummies. "
                        "Danish sweet roll sweet tootsie roll cake chupa chups bonbon toffee brownie. "
                        "Soufflé sweet roll pastry candy canes. "
                        "Powder bonbon halvah jujubes lollipop brownie tootsie roll. "
                        "Fruitcake halvah ice cream dessert sugar plum jelly-o chupa chups. "
                        "Cake lemon drops dragée dragée biscuit brownie lemon drops.</p>")

    db.session.add(post)
    db.session.commit()

    click.echo('initialized the Hello World post')


# drop post
@click.command()
@click.option('-p', '--post-public-id', prompt="Post Public ID", required=True)
def drop_post(post_public_id):
    post = Post.query.filter_by(post_public_id=post_public_id).first()

    if post:
        db.session.delete(post)
        db.session.commit()

        click.echo('{} post has been removed successfully from dashboard'.format(
            post.post_public_id))
    else:
        click.echo('{} post public id does\'nt exist'.format(post))


# Drop User from Dashboard
@click.command()
@click.option('-u', '--user-public-id', prompt='User Public ID', required=True)
def drop_user(user_public_id):
    user = User.query.filter_by(user_public_id=user_public_id).first()

    if user and user.admin is True:
        db.session.delete(user)
        db.session.commit()

        click.echo(
            '{} user has been removed successfully from dashboard'.format(user_public_id))
    else:
        click.echo('you have not permission to execute this command')


cli.add_command(init_db)
cli.add_command(init_admin)
cli.add_command(add_admin)
cli.add_command(init_user)
cli.add_command(init_category)
cli.add_command(add_category)
cli.add_command(drop_category)
cli.add_command(init_post)
cli.add_command(drop_post)
cli.add_command(drop_user)

if __name__ == '__main__':
    cli()
