import click
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
from slugify import slugify

from moxart import create_app, db
from moxart.models.user import User
from moxart.models.post import Post
from moxart.models.category import Category

app = create_app()
app.app_context().push()


@click.group()
def cli():
    pass


# Initializing Database
@click.command()
def init_db():
    db.create_all()
    click.echo('[ Initialized the Database ]')


# Initializing an Admin User
@click.command()
def init_admin():
    if db.session.query(User.username).filter_by(
            username=app.config['ADMIN_USERNAME']
    ).scalar() is None:
        admin = User(
            username=app.config['ADMIN_USERNAME'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD'],
            admin=True
        )
        db.session.add(admin)
        db.session.commit()
        click.echo('[ Initialized The Admin User ]')
    else:
        click.echo('[ User Admin is Already Exists ]')


# Initializing a User
@click.command()
@click.option('-u', '--username', prompt='Username', required=True)
@click.option('-e', '--email', prompt='Email')
@click.option('-p', '--password', prompt='Password', hide_input=True,
              confirmation_prompt=True, required=True)
def init_user(username, email, password):
    if db.session.query(User.username).filter_by(
            username=username
    ).scalar() is None:
        user = User(
            username=username, email=email, password=password, admin=False
        )
        db.session.add(user)
        db.session.commit()
        click.echo('[ {} user has been created successfully ]'.format(username))
    else:
        click.echo('[ The {} has already been taken ]'.format(username))


# Initializing uncategorized category
@click.command()
def init_category():
    category = Category(category_name="Uncategorized", category_name_slug=slugify("Uncategorized"))

    db.session.add(category)
    db.session.commit()

    click.echo('[ Initialized The Uncategorized Category ]')


# Initializing Hello World Post
@click.command()
def init_post():
    user = User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first()
    category = Category.query.filter_by(category_name_slug="uncategorized").first()

    post = Post(
        user_public_id=user.user_public_id, category_public_id=category.category_public_id,
        title="Hello, World!",
        title_slug="hello-world!",
        content="<p>Pie sugar plum pie pudding. Caramels lemon drops jelly-o croissant tart.</p>"
    )

    db.session.add(post)
    db.session.commit()

    click.echo('[ Initialized The Hello World Post ]')


# Drop User from Dashboard
@click.command()
@click.option('-u', '--username', prompt='Username', required=True)
def drop_user(username):
    if username != 'admin':
        if db.session.query(User.username).filter(User.username == username):
            db.session.query(User.username).filter(
                User.username == username
            ).delete()
            db.session.commit()
            click.echo(
                '[ {} user has been removed successfully from dashboard ]'.format(username))
        else:
            click.echo('[ {} user does\'nt exist ]'.format(username))
    else:
        click.echo('[ You can\'t delete an Admin user ]')


cli.add_command(init_db)
cli.add_command(init_admin)
cli.add_command(init_user)
cli.add_command(init_category)
cli.add_command(init_post)
cli.add_command(drop_user)

if __name__ == '__main__':
    cli()
