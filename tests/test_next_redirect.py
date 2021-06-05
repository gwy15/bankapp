from tests import *
from urllib.parse import urlencode


def test_get_login_with_ok_next(client):
    r = client.get('/login')
    assert r.status_code == 200

    r = client.get('/login?next=/')
    assert r.status_code == 200

    r = client.get('/login?next=/register')
    assert r.status_code == 200

    r = client.get('/login?next=/admin')
    assert r.status_code == 200

    r = client.get('/login?next=/register')
    assert r.status_code == 200


def test_get_login_with_bad_next(client: Client):
    query = urlencode({'next': 'https://example.com'})
    r = client.get('/login?' + query)
    assert r.status_code == 400

    query = urlencode({'next': 'http://example.com'})
    r = client.get('/login?' + query)
    assert r.status_code == 400
