from http import HTTPStatus

from fastapi.testclient import TestClient

from index_libri.app import app


def test_root_retorna_200_ok_e_index_libri():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'index libri api'}
