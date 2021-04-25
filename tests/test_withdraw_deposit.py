from tests import *


def test_withdraw_not_login(client):
    r = client.post('/withdraw', data={
        'amount': 0
    }, follow_redirects=True)
    assert b'login' in r.data


def test_withdraw_invalid_amount(client):
    login(client)
    # client has 0 balance
    for amount in [0, '-1', '-0.01', '4294967296.00']:
        r = client.post('/withdraw', data={
            'amount': amount
        }, follow_redirects=True)
        assert b'invalid as currency amount.' in r.data


def test_deposit_with_invalid_amount(client):
    login(client)
    # client has 0 balance
    for amount in [0, '-1', '-0.01', '4294967296.00']:
        r = client.post('/deposit', data={
            'amount': amount
        }, follow_redirects=True)
        assert b'invalid as currency amount.' in r.data


def test_deposit_ok(client):
    login(client)
    for amount in ['1.00', '10.00', '100.0', '4294967184.99']:
        r = client.post('/deposit', data={
            'amount': amount
        })
        assert b'success.' in r.data


def test_withdraw_ok(client):
    login(client)

    r = client.post('/deposit', data={'amount': '4294967295.99'})
    assert b'success' in r.data

    for amount in ['1.00', '10.00', '100.0', '4294967184.99']:
        r = client.post('/withdraw', data={
            'amount': amount
        })
        assert b'success.' in r.data


def test_deposit_overflow(client):
    login(client)

    r = client.post('/deposit', data={'amount': '4294967295.99'})
    assert b'success' in r.data

    r = client.post('/deposit', data={'amount': '0.01'})
    assert b'The balance is too big.' in r.data


def test_withdraw_overflow(client):
    login(client)

    r = client.post('/deposit', data={'amount': '10.00'})
    assert b'success' in r.data

    r = client.post('/withdraw', data={'amount': '10.01'})
    assert b'have enough balance to make this withdraw.' in r.data
