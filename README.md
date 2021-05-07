# Bankapp
[![Test](https://github.com/gwy15/bankapp/actions/workflows/test.yml/badge.svg)](https://github.com/gwy15/bankapp/actions/workflows/test.yml)
[![Build Docker](https://github.com/gwy15/bankapp/actions/workflows/docker.yml/badge.svg)](https://github.com/gwy15/bankapp/actions/workflows/docker.yml)

The bankapp is a web app that is built on flask web framework. It is developed as the project for course SWE-266 (Software Security and Dependability).

The app supports the following functions
- Register with an initial balance
- Login an existing account
- Withdraw some amount of money from the bank
- Deposit some amount of money from the bank
- Look at the most recent 15 transactions

Please note that currently it does not support logout. You might wanna use the Incognito Window feature
in your browser.

# Prepare Environment

First, prepare your environment. You'll need python3.9 and poetry, which by the way is a 
nice tool to manage python project, installed on your computer.

I'll skip installing python3.9. You can find the instructions to install poetry [here].

[here]: https://pypi.org/project/poetry/#Installation

After you get these two basic dependencies, run the following command
to setup your workspace:

```bash
poetry install
```

# Development

Run the following command to run the app
```
poetry run flask run
```

Visit http://127.0.0.1:5000/ to start the app.

This will launch the app in development mode and hot-reload will be enabled.

# Test
To run unit-tests, run
```bash
poetry run pytest tests -v
```

# Deployment
The bankapp only supports deployment on Linux.

On linux, run
```
poetry run gunicorn bankapp:app
```
to start the app in development mode.

## ⚠️ Warning ⚠️
- Do not use `flask run` for production.
- This app is not designed to be run on Windows for production.
- Before deployment, create a `config.local.py` beside `config.py`. You should overwrite the `SECRET_KEY` value to a strong, random generated secret.


# Develop by Docker
Build the docker image:
```
docker build . -t bankapp
```
Run the docker image:
```
docker run -it --rm -p 80:80 bankapp
```
