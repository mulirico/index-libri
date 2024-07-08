from http import HTTPStatus


def test_create_conta(client):
    response = client.post(
        '/contas',
        json={
            'username': 'mujica',
            'email': 'mujica@test.com',
            'password': 'segredo',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'mujica',
        'email': 'mujica@test.com',
        'id': 1,
    }


def test_read_conta(client):
    response = client.get('/contas/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'contas': [
            {
                'username': 'mujica',
                'email': 'mujica@test.com',
                'id': 1,
            }
        ]
    }


def test_update_conta_nao_registrada(client):
    response = client.put('/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_update_user(client):
    response = client.put(
        '/contas/1',
        json={
            'username': 'mujica',
            'email': 'mujica@test.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'mujica',
        'email': 'mujica@test.com',
        'id': 1,
    }


def test_delete_conta_nao_registrada(client):
    response = client.delete('/contas/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_delete_conta(client):
    response = client.delete('/contas/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}
