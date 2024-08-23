from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings

settings = Settings()


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, settings.SECRET_KEY, [settings.ALGORITHM])

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


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_get_token_user_inexistent(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong@email.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'email or password is incorrect'}


def test_delete_user_no_token(client):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Not authenticated',
    }


def test_update_user_no_token(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'new username',
            'password': 'new password',
            'email': 'newemail@tester.com',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Not authenticated',
    }