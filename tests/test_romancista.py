from http import HTTPStatus

from tests.conftest import RomancistaFactory


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


def test_read_romancista_id(client, autora, token):
    response = client.get(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': autora.id,
        'nome': autora.nome,
    }


def test_read_romancista_inexistent(client, token):
    response = client.get(
        '/romancista/0', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_read_romancista_return_2(client, token, session):
    expected_romancistas = 2
    session.bulk_save_objects(RomancistaFactory.create_batch(2))
    session.commit()

    response = client.get(
        '/romancista/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_read_romancista_limit_return_2(client, token, session):
    expected_romancistas = 2
    session.bulk_save_objects(RomancistaFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/romancista/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_read_romancista_with_nome_return_2(client, token, session):
    expected_romancistas = 1
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='Mujica'))
    session.commit()

    response = client.get(
        '/romancista/?nome=Mujica',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_patch_romancista_error(client, token):
    response = client.patch(
        '/romancista/0',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_romancista(client, token, session, autora):
    session.add(autora)
    session.commit()

    response = client.patch(
        f'/romancista/{autora.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'novo nome',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': autora.id,
        'nome': 'novo nome',
    }


def test_delete_romancista(client, token, autora, session):
    session.add(autora)
    session.commit()

    response = client.delete(
        f'/romancista/{autora.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletada no MADR'}


def test_delete_romancista_inexistent(client, token):
    response = client.delete(
        '/romancista/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}
