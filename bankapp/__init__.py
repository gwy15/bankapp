from bankapp import account, models
from flask import Flask, render_template
from flask_login import login_required
__version__ = '0.1.0'

import logging
logger = logging.getLogger()


def initapp() -> Flask:
    app = Flask(__name__, template_folder='../templates')

    app.config.from_pyfile('./config.py')
    app.config.from_pyfile('./config.local.py', silent=True)

    models.db.init_app(app)
    account.login_manager.init_app(app)

    with app.app_context():
        models.db.create_all()

    app.register_blueprint(account.bp)

    return app


app = initapp()


@app.route('/')
@login_required
def index():
    return render_template('index.html')
