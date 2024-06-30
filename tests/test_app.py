from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo_e_batata(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_hello_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/hello/')
    assert response.status_code == HTTPStatus.OK
    assert response.text == 'Olá mundo!'


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
        'ID': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'username',
                'email': 'email@tester.com',
                'ID': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'new username',
            'password': 'new password',
            'email': 'newemail@tester.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'new username',
        'email': 'newemail@tester.com',
        'ID': 1,
    }


def test_update_user_nonexistent(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'new username',
            'password': 'new password',
            'email': 'newemail@tester.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


def test_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'new username',
        'email': 'newemail@tester.com',
        'ID': 1,
    }


def test_get_user_nonexistent(client):
    response = client.get('/users/0')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }



def test_delete_user(client):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted!',
    }


def test_delete_user_nonexistent(client):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }
