Blapp
=====
[![Build Status](https://travis-ci.org/litheblas/blapp.svg?branch=master)](https://travis-ci.org/litheblas/blapp)
[![Docker Repository](https://quay.io/repository/litheblas/blapp/status "Docker Repository")](https://quay.io/repository/litheblas/blapp)

The Blapp is the LiTHe Blås App. It handles very important things.

# Installing dependencies
## macOS
Use Homebrew and Pipenv:
```sh
brew bundle install
pipenv install -d -e . (Don't leave out the period)
```

## Other platforms
Pull requests with instructions are welcome. The instructions above and the
`Brewfile` will give you a hint of what's needed.

## Linux
sudo apt install chromium-chromedriver
sudo pip install mysqlclient
sudo apt install libmysqlclient-dev
sudo pip install pipenv
sudo apt install postgresql postgresql-contrib
sudo apt install python3.6-dev
sudo apt install redis-server (might need extra config.)
sudo apt install yarnpkg (might need to add rep.)

# Setting up a development environment
Copy the environment template, migrate the database and start an interactive
Python shell:
```sh
cp .env.template .env
pipenv run django-admin migrate
pipenv run django-admin shell_plus
```

In the Python shell, with your own values, run the following and quit with Ctrl+D:
```py
UserAccount.objects.create_superuser(
    first_name='Olle',
    last_name='Vidner',
    username='knulle',
    email='olle@vidner.se',
    password='abcdefgh',
)
```

Now you're ready to run the development server:
```sh
pipenv run django-admin runserver
```

The development server should now be available at http://localhost:8000.

# Running tests
```sh
pipenv run pytest
```

# Tips and tricks
* If you prefer not to prefix commands with `pipenv run`, then start a subshell
within the virtual environment with `pipenv shell`.

# Documented errors:

## Mac:

If the `postgresql` service isn't running. In that case, the following command should start it.
```sh
sudo brew services postgresql start
```

## Database:

If you get the error: "FATAL: role "blapp" does not exist", you may need to enter the postgres prompt and create the database blapp with an owner blapp. On mac, the following commands may be a possible solution (from the parent blapp directory). Don't leave out the semicolons.
```sh
psql -U postgres -h localhost
=# CREATE USER blapp SUPERUSER;
=# CREATE DATABASE blapp WITH OWNER blapp;
=# \q
```
After this, the migrate command should work.