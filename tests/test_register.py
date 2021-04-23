from tests import *


def test_get_register_page(client):
    r = client.get('/register')
    assert b'register' in r.data


def test_register_account_with_csrf():
    for client in make_client(csrf=True):
        r = client.post('/register', data={
            'username': 'admin2',
            'password': 'password123'
        })
        assert b'CSRF token is missing' in r.data


def test_register_ok(client):
    r = client.post('/register', data={
        'username': 'guest',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Hi, guest' in r.data


def test_register_existing_account(client):
    r = client.post('/register', data={
        'username': 'admin',
        'password': '123123123'
    })
    assert b'username is already taken' in r.data


def test_register_with_improper_input(client):
    r = client.post('/register', data={})
    assert b'username error: This field is required.' in r.data
    assert b'password error: This field is required.' in r.data

    r = client.post('/register', data={
        'username': '1',
        'password': '1'
    })
    assert b'username error: Field must be between 3 and 20 characters long.' in r.data
    assert b'password error: Field must be between 9 and 36 characters long.' in r.data

    r = client.post('/register', data={
        'username': '~~~~~~',
        'password': '~~~~~~~~~~~~'
    })
    assert b'username error: Invalid input.' in r.data
    assert b'password error: Invalid input.' in r.data
