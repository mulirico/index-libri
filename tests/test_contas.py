from http import HTTPStatus

from index_libri.schemas import ContaPublic


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


def test_create_conta_with_exist_username(client, user):
    response = client.post(
        '/contas',
        json={
            'username': 'Teste',
            'email': 'novoteste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username já registrado'}


def test_create_conta_with_exist_email(client, user):
    response = client.post(
        '/contas',
        json={
            'username': 'NovoTeste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já registrado'}


def test_read_conta_with_users(client, user):
    user_schema = ContaPublic.model_validate(user).model_dump()
    response = client.get('/contas/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'contas': [user_schema]}


# def test_read_conta_with_id(client, user):
#     user_schema = ContaPublic.model_validate(user).model_dump()
#     response = client.get('/contas/{user.id}')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'conta': [user_schema]}


def test_update_conta_nao_registrada(client, user):
    response = client.put(
        '/contas/2',
        json={
            'username': 'mujica',
            'email': 'mujica@test.com',
            'password': 'novasenha',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user(client, user):
    response = client.put(
        '/contas/1',
        json={
            'username': 'mujica',
            'email': 'mujica@test.com',
            'password': 'novasenha',
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
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_delete_conta(client, user):
    response = client.delete('/contas/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}
