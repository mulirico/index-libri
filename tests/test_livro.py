from http import HTTPStatus

from tests.conftest import LivroFactory


def test_create_livro(client, token, autora):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'tarde no quintal',
            'ano': 1998,
            'id_romancista': autora.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'ano': 1998,
        'titulo': 'tarde no quintal',
        'id_romancista': autora.id,
    }


def test_create_livro_existente(client, token, livro):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': livro.titulo,
            'ano': livro.ano,
            'id_romancista': 1,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Livro já consta no MADR',
    }


def test_create_livro_without_romancista(client, token):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'Não existe',
            'ano': 10,
            'id_romancista': -1,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Romancista não encontrado, insira a autoria primeiro',
    }


def test_get_livro_by_id(client, token, livro):
    response = client.get(
        f'/livro/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'titulo': livro.titulo,
        'ano': livro.ano,
        'id_romancista': livro.id_romancista,
    }


def test_get_livro_by_id_inexistent(client, token):
    response = client.get(
        '/livro/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Livro não consta no MADR',
    }


def test_read_livro_return_3(client, token, session, livro):
    expected_livros = 3
    session.add(livro)
    session.bulk_save_objects(LivroFactory.create_batch(2))
    session.commit()

    response = client.get(
        '/livro/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_read_livro_return_limit_2(client, token, session, livro):
    expected_livros = 2
    session.add(livro)
    session.bulk_save_objects(LivroFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/livro/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_read_livro_titulo(client, token, session, livro):
    expected_livros = 1
    session.add(livro)
    session.bulk_save_objects(LivroFactory.create_batch(1, titulo='titulo'))
    session.commit()

    response = client.get(
        '/livro/?titulo=titulo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_read_livro_ano(client, token, session, livro):
    expected_livros = 1
    session.add(livro)
    session.bulk_save_objects(LivroFactory.create_batch(1, ano=1111))
    session.commit()

    response = client.get(
        '/livro/?ano=1111',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_read_livro_idromancista(client, token, session, livro):
    expected_livros = 2
    session.add(livro)
    session.bulk_save_objects(LivroFactory.create_batch(1, id_romancista=1))
    session.commit()

    response = client.get(
        '/livro/?id_romancista=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_read_livro_filters_combined(client, token, session, livro):
    expected_livros = 1
    session.add(livro)
    session.bulk_save_objects(
        LivroFactory.create_batch(1, titulo='mujica', ano=10)
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(1, titulo='mujica testando', ano=1010)
    )
    session.commit()

    response = client.get(
        '/livro/?titulo=mujica&ano=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['livros']) == expected_livros


def test_patch_livro_error(client, token):
    response = client.patch(
        '/livro/0',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_livro(client, token, livro, session):
    session.add(livro)
    session.commit()

    response = client.patch(
        f'/livro/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': 'novo titulo'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'titulo': 'novo titulo',
        'ano': livro.ano,
        'id_romancista': livro.id_romancista,
    }


def test_delete_livro_erro(client, token):
    response = client.delete(
        '/livro/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_delete_livro(client, token, livro, session):
    session.add(livro)
    session.commit()

    response = client.delete(
        f'/livro/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}
