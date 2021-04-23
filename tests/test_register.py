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
    # all the following balances should be accepted.
    balances = [
        '0.12', '0.00', '0', '.0', '10.0', '4294967295.99'
    ]
    for balance in balances:
        username = f'guest_{balance}'
        r = client.post('/register', data={
            'username': username,
            'password': 'password123',
            'balance': balance
        }, follow_redirects=True)
        assert f'Hi, {username}'.encode() in r.data


def test_register_existing_account(client):
    r = client.post('/register', data={
        'username': 'admin',
        'password': '123123123',
        'balance': '0.12'
    })
    assert b'username is already taken' in r.data


def test_register_with_illegal_balance(client):
    illegal_balances = ['-10', '-0.1', '4294967296',
                        '1.123', '1e1', '0x2', '0.0000', ]
    for balance in illegal_balances:
        r = client.post('/register', data={
            'username': f'guest_{balance}',
            'password': 'password123',
            'balance': balance
        }, follow_redirects=True)
        assert b'balance error: This number is invalid as currency amount' in r.data, balance


def test_register_with_improper_input(client):
    r = client.post('/register', data={})
    assert b'username error: This field is required.' in r.data
    assert b'password error: This field is required.' in r.data
    assert b'balance error: This field is required.' in r.data

    r = client.post('/register', data={
        'username': 'a' * 128,
        'password': 'b' * 128
    })
    assert b'username error: Field must be between 1 and 127 characters long.' in r.data
    assert b'password error: Field must be between 1 and 127 characters long.' in r.data

    r = client.post('/register', data={
        'username': '~~~~~~',
        'password': '~~~~~~~~~~~~'
    })
    assert b'username error: Invalid input.' in r.data
    assert b'password error: Invalid input.' in r.data
