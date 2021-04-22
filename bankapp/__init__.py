from bankapp import account, models
from flask import Flask, render_template
__version__ = '0.1.0'

import logging
logger = logging.getLogger()


def initapp() -> Flask:
    app = Flask(__name__, template_folder='../templates')

    app.config.from_pyfile('./config.py')
    app.config.from_pyfile('./config.local.py', silent=True)

    models.Base.metadata.create_all(bind=models.engine)

    app.register_blueprint(account.bp)

    return app


app = initapp()


@app.route('/')
# TODO: login required
def index():
    return render_template('index.html')
