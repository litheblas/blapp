Blapp
=====
[![Build Status](https://travis-ci.org/litheblas/blapp.svg?branch=master)](https://travis-ci.org/litheblas/blapp)

The Blapp is the LiTHe Blås App. It handles very important things.

# Installing dependencies
## macOS
Use Homebrew and Pipenv:
```sh
brew bundle install
pipenv install -d
```

## Other platforms
Pull requests with instructions are welcome. The instructions above and the
`Brewfile` will give you a hint of what's needed.

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
