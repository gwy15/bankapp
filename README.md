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

# Run

For windows run the following command to run the app
```bash
$env:FLASK_APP="bankapp"
$env:FLASK_ENV="development"
poetry run flask run
```

For macos users, run these instead:
```bash
export FLASK_APP="bankapp"
export FLASK_ENV="development"
poetry run flask run
```

# Test
To run unit-tests, run
```bash
poetry run pytest tests -v
```

# TODO
- [ ] finer background pattern

# vulnerabilities
- hint: next
