# Bankapp
[![Test](https://github.com/gwy15/bankapp/actions/workflows/test.yml/badge.svg)](https://github.com/gwy15/bankapp/actions/workflows/test.yml)

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

# Developement

For windows run the following command to run the app
```bash
poetry run flask run
```

For macos / linux users, run these instead:
```bash
poetry run flask run
```

This will launch the app in development mode and hot-reload will be enabled.

# Test
To run unit-tests, run
```bash
poetry run pytest tests -v
```

# Deployment
On linux,
```
poetry run gunicorn bankapp:app
```

## ⚠️ Warning ⚠️
- Do not use `flask run` for production.
- This app is not designed to be run on Windows for production.
- Before deployment, create a `config.local.py` in the directory.

# TODO
- [x] finer background pattern

# vulnerabilities
- hint: next
- hint: secret
