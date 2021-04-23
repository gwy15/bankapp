import flask
import pytest
import bankapp
from typing import Generator


def make_client(csrf: bool) -> Generator[flask.testing.FlaskClient, None, None]:
    app = bankapp.createapp(with_db=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = csrf
    with app.test_client() as client:
        with app.app_context():
            bankapp.models.init_app(app)
            bankapp.models.User.create('admin', 'adminpswd')
        client: flask.testing.FlaskClient
        yield client


@pytest.fixture
def client() -> Generator[flask.testing.FlaskClient, None, None]:
    for client in make_client(csrf=False):
        yield client


def login(client):
    r = client.post('/login', data={
        'username': 'admin',
        'password': 'adminpswd'
    })
    assert b'Redirecting' in r.data
    assert r.status_code == 302
