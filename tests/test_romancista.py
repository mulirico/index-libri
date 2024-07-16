from http import HTTPStatus


def test_create_romancista(client, user, token):
    response = client.post(
        f'/romancista/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'Clarice Lispector',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Clarice Lispector',
    }


def test_create_romancista_with_autora(client, autora, user, token):
    response = client.post(
        f'/romancista/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': autora.nome,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_create_romancista_without_permission(
    client, other_user, autora, token
):
    response = client.post(
        f'/romancista/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': autora.nome},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
