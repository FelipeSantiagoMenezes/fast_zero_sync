from http import HTTPStatus

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'username',
            'password': 'password',
            'email': 'email@tester.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'username',
        'email': 'email@tester.com',
        'id': 1,
    }


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'uniqueUsername',
            'email': user.email,
            'password': 'uniquePassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'email already exist'}


def test_create_user_with_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'unique@email.com',
            'password': 'uniquePassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'username already exist'}


def test_read_users_with_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_unauthorized(client, user, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'new username',
            'password': 'new password',
            'email': 'newemail@tester.com',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permision'}


def test_jwt_no_user(client, user):
    data = {'sub': 'nonexist@aliens.com'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_inexistent(client):
    response = client.get(
        '/users/1',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted!',
    }


def test_jwt_invalid(client, user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer wrongtoken'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_unauthorized(client, user, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permision'}


def test_jwt_no_sub(client, user):
    data = {}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_no_token(client, user):
    response = client.delete(
        f'/users/{user.id}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Not authenticated',
    }


def test_update_user_no_token(client, user, other_user):
    response = client.put(
        f'/users/{other_user.id}',
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
