from http import HTTPStatus


def test_create_romancista(client, token):
    response = client.post(
        '/romancista',
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


def test_create_romancista_with_autora(client, autora, token):
    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': autora.nome,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_create_romancista_without_permission(client, autora):
    response = client.post(
        '/romancista',
        headers={'Authorization': 'Bearer $token invalido'},
        json={'nome': autora.nome},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
