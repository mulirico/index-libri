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
            'username': user.username,
            'email': user.email,
            'password': user.hashed_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username já registrado'}


def test_create_conta_with_exist_email(client, user):
    response = client.post(
        '/contas',
        json={
            'username': 'teste',
            'email': user.email,
            'password': user.hashed_password,
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


def test_update_user(client, user, token):
    response = client.put(
        f'/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_update_conta_without_permission(client, other_user, token):
    response = client.put(
        f'/contas/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'mujica',
            'email': 'mujica@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Não autorizado'}


def test_delete_conta(client, user, token):
    response = client.delete(
        f'/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_conta_without_permission(client, other_user, token):
    response = client.delete(
        f'/contas/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Não autorizado'}
