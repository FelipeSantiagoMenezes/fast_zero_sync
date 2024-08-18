from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, [ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer wrongtoken'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_no_sub(client):
    data = {}
    token = create_access_token(data)
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_no_user(client):
    data = {'sub': 'nonexist@aliens.com'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
