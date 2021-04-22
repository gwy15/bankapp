import flask
import pytest
import bankapp


@pytest.fixture
def client():
    bankapp.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    bankapp.app.config['TESTING'] = True
    with bankapp.app.test_client() as client:
        with bankapp.app.app_context():
            bankapp.models.db.init_app(bankapp.app)
        client: flask.testing.FlaskClient
        yield client


def test_index_with_no_login(client):
    r = client.get('/')
    assert b'login' in r.data
