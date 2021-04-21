__version__ = '0.1.0'

from flask import Flask, render_template
from . import account


def initapp() -> Flask:
    app = Flask(__name__, template_folder='../templates')
    app.register_blueprint(account.bp)

    import bankapp.models
    models.Base.metadata.create_all(bind=models.engine)

    return app


@app.route('/')
def index():
    return render_template('base.html')
