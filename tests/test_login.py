from tests import *


def data(username='admin', password='adminpswd'):
    return {
        'data': {
            'username': username,
            'password': password
        }
    }


def test_get_login_page(client):
    r = client.get('/login')
    assert b'login' in r.data


def test_login_with_csrf():
    for client in make_client(csrf=True):
        r = client.post('/login', **data())
        assert b'CSRF token is missing' in r.data


def test_login_ok(client):
    r = client.post('/login', **data(), follow_redirects=True)
    assert b'Welcome, admin' in r.data


def test_login_with_wrong_password(client):
    r = client.post('/login', **data(password='123123123'),
                    follow_redirects=True)
    assert b'user does not exist' in r.data
    assert b'wrong password' in r.data


def test_login_with_non_existing_account(client):
    r = client.post('/login', **data(username='123123123'),
                    follow_redirects=True)
    assert b'user does not exist' in r.data
    assert b'wrong password' in r.data


def test_login_with_improper_input(client):
    r = client.post('/login', data={})
    assert b'username error: This field is required.' in r.data
    assert b'password error: This field is required.' in r.data

    r = client.post('/login', data={
        'username': '1',
        'password': '1'
    })
    assert b'username error: Field must be between 3 and 20 characters long.' in r.data
    assert b'password error: Field must be between 9 and 36 characters long.' in r.data

    r = client.post('/login', data={
        'username': '~~~~~~',
        'password': '~~~~~~~~~~~~'
    })
    assert b'username error: Invalid input.' in r.data
    assert b'password error: Invalid input.' in r.data
