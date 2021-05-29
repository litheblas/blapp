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

## Ubuntu (WSL Ubuntu 20.04 LTS)
```sh
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install \
    chromium-chromedriver \
    libmysqlclient-dev \
    postgresql \
    postgresql-contrib \
    python3.6-dev \
    python3-pip \
    redis-server \
    yarnpkg

sudo pip3 install \
    mysqlclient \
    pipenv

pipenv install -d -e .
```

## Other platforms
Pull requests with instructions are welcome. The instructions above and the
`Brewfile` will give you a hint of what's needed.

# Setting up a development environment
Most of these commands are for Ubuntu, but with minor modifications it should work on other systems.

## Configure PostgreSQL
Start the postgres service with:
```sh
# Linux:
sudo service postgresql start

# Mac:
sudo brew services postgresql start
```

Enter the postgres shell and add a user and database:
```sh
# Linux:
sudo su - postgres
psql \
    -c 'CREATE ROLE blapp SUPERUSER LOGIN;' \
    -c 'CREATE DATABASE blapp WITH OWNER blapp;' \
    -c 'SHOW hba_file;'

# Mac (may not work):
psql -U postgres -h localhost
=# CREATE USER blapp SUPERUSER;
=# CREATE DATABASE blapp WITH OWNER blapp;
=# SHOW hba_file;
=# \q
```
The path that is printed is the path to the `hba_file` file. It should be something like `/etc/postgresql/12/main/pg_hba.conf`.

In that file, change the `METHOD` under the lines
- \# "local" is for Unix domain socket connections only
- \# IPv4 local connections:
- \# IPv6 local connections:

to `trust`. The end of the file should look something like this:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
```

Press `Ctrl+D` to exit the postgres shell.

Restart the postgres service for the changes to take effect:
```sh
# Linux:
sudo service postgresql restart

# Mac:
sudo brew services postgresql restart
```

## Configure Django
Copy the environment template, migrate the database and start an interactive
Python shell:
```sh
cp .env.template .env
pipenv run django-admin migrate
pipenv run django-admin shell_plus
```

In the Python shell, with your own values, run the following and quit with `Ctrl+D`:
```py
UserAccount.objects.create_superuser(
    first_name='Olle',
    last_name='Vidner',
    username='knulle',
    email='olle@vidner.se',
    password='abcdefgh',
)
```
Now the development server should be configured correctly.

# Start the development server
Make sure that the postgres service is running:
```sh
# Linux:
sudo service postgresql start

# Mac:
sudo brew services postgresql start
```

Start redis:
```sh
redis-server &
```
Double check that redis is running with the port `6379`. If not, start redis with `redis-server --port 6379 &` instead. The `&` starts the server in the background. To stop redis, run `fg` to connect to the process and then press `Ctrl+C`.

Now you're ready to start the django server:
```sh
pipenv run django-admin runserver
```

The development server should now be available at http://localhost:8000/admin.

# Running tests
```sh
pipenv run pytest
```

# Tips and tricks
* If you prefer not to prefix commands with `pipenv run`, then start a subshell
within the virtual environment with `pipenv shell`.

# Documented errors:

## PostgreSQL not started:
If you get the error
```
Is the server running locally and accepting
        connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
```
then the `postgresql` service isn't running. The commands for starting it can be found under [Configure PosgreSQL](#Configure-PostgreSQL)


## Database does not exist:

If you get the error: `FATAL: role "blapp" does not exist`, then the database has not been created. Follow the instructions under [Configure PosgreSQL](#Configure-PostgreSQL)
