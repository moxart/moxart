# :seedling: Moxart Panel :seedling:

-  :warning: Under Construction
- 🔭 I’m currently working on Flask

```
$ cd moxart-panel
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ chmod -x init.sh
```

## :hurtrealbad: Hard Setup

### Config File
edit `config.py` in *instance* 
* Default **ADMIN_USERNAME** is `moxart`
* Default **ADMIN_PASSWORD** is `password`
> SETUP EMAIL IS REQUIRED

### Initializing MySQL Database

`$ bash init.sh`


### Useful Commands

`$ python3 manage.py --help`

```
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-admin
  add-category
  drop-category
  drop-directory
  drop-post
  drop-user
  init-admin
  init-category
  init-db
  init-directory
  init-post
  init-user
  show-users
  show-users-activity
  show-users-alt

```

### Run The Flask Server
`$ flask run`

### Send Request To API
If everything goes well then you should be able to send request to API with **cURL** or other methods such as **Postman** app

`curl -H "Content-Type: application/json" -d '{"username": "moxart", "password": "password"}' http://localhost:5000/login`

and your output should be something like this:

```
{
  "status": 200, 
  "login": true, 
  "msg": "user has been authenticated successfully", 
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYzNDgzMzgsIm5iZiI6MTYwNjM0ODMzOCwianRpIjoiNWE4YmYwZDctMGJjYy00YTYzLWFlODQtZWM3YjY0NDJiYjIxIiwiaWRlbnRpdHkiOiJtb3hhcnQiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJyb2xlcyI6ImFkbWluIn19.0f2JLU7FOV3r3TRbSJcbp3-iTuAToN_onu7umV4uBNs", 
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYzNDgzMzgsIm5iZiI6MTYwNjM0ODMzOCwianRpIjoiOTc0YWYxYjktNDE4Zi00YWNkLTkxZGMtMDY0ODZjZDVjY2M1IiwiZXhwIjoxNjA4OTQwMzM4LCJpZGVudGl0eSI6Im1veGFydCIsInR5cGUiOiJyZWZyZXNoIn0.72gCoipzkuvAmiffqNLh2jn9FYIfe2r51x4X67x5_MQ"
}

```
