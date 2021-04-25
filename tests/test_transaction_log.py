from tests import *


def test_transaction_log(client):
    login(client)
    r = client.get('/transactions')
    assert b'Latest 1 Transaction' in r.data

    # now make some transactions
    for amount in ['12', '234.12', '99828']:
        r = client.post('/deposit', data={'amount': amount})
        assert b'success' in r.data
        r = client.get('/transactions')
        assert amount in r.data.decode()

    for amount in ['2.12', '7.23', '9.99']:
        r = client.post('/withdraw', data={'amount': amount})
        assert b'success' in r.data
        r = client.get('/transactions')
        assert amount in r.data.decode()
