FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Installing poetry..." \
    && curl -sSL https://raw.fastgit.org/python-poetry/poetry/master/get-poetry.py | python \
    && mkdir /code

COPY . /code/

RUN . $HOME/.poetry/env \
    && python --version \
    && poetry --version \
    && which poetry \
    && cd /code \
    && poetry install

WORKDIR /code
ENTRYPOINT [ "/root/.poetry/bin/poetry", "run" ]
CMD [ "gunicorn", "bankapp:app", "--bind", "0.0.0.0:80", "-w", "8" ]
