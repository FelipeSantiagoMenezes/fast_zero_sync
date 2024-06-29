from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo_e_batata():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensage': 'Olá mundo!', 'batata': 'batata'}


def test_hello_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/hello/')
    assert response.status_code == HTTPStatus.OK
    assert response.text == 'Olá mundo!'
