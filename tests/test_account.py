from tests import *


def test_index_with_no_login(client):
    r = client.get('/')
    assert b'login' in r.data


def test_register_account():
    for client in make_client(True):
        r = client.post('/register', data={
            'username': 'admin',
            'password': 'password123'
        })
        assert b'CSRF token is missing' in r.data


def test_register(client):
    r = client.get('/register')
    assert b'register' in r.data

    r = client.post('/register', data={
        'username': 'admin',
        'password': 'password123'
    })
    assert b'Redirecting' in r.data
