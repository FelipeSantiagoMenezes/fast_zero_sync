from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_hello_deve_retornar_ok_e_html_ola_mundo(client):
    response = client.get('/hello/')
    assert response.status_code == HTTPStatus.OK
    assert response.text == '<h1>Olá mundo!<h1>'
