from tests import *


def test_index_with_no_login(client):
    r = client.get('/')
    assert b'login' in r.data


def test_index_with_login(client):
    login(client)
    r = client.get('/', follow_redirects=True)
    assert b'Welcome, admin' in r.data
