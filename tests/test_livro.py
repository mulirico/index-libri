from http import HTTPStatus


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
            'id_romancista': livro.id_romancista,
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
