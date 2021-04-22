import flask
import pytest
import bankapp


def make_client(csrf: bool):
    app = bankapp.initapp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = csrf
    with app.test_client() as client:
        with app.app_context():
            bankapp.models.db.init_app(app)
            bankapp.models.db.create_all()
        client: flask.testing.FlaskClient
        yield client


@pytest.fixture
def client():
    for c in make_client(csrf=False):
        yield c
