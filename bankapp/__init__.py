from bankapp import account, models, index
from bankapp.logging import init_logging
from flask import Flask
from flask_login import login_required
from pathlib import Path

__version__ = '0.1.0'

import logging
init_logging()
logger = logging.getLogger()


def createapp(with_db: bool = True) -> Flask:
    app = Flask(__name__, template_folder=str(Path('./templates').absolute()))

    app.config.from_pyfile('./config.py')
    app.config.from_pyfile('./config.local.py', silent=True)

    if with_db:
        models.init_app(app)
    account.login_manager.init_app(app)

    app.register_blueprint(index.bp)
    app.register_blueprint(account.bp)

    return app


app = createapp()
