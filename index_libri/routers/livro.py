from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import Livro, Romancista, User
from index_libri.schemas import (
    LivroList,
    LivroPublic,
    LivroSchema,
    LivroUpdate,
    Message,
)
from index_libri.security import get_current_user

router = APIRouter(prefix='/livro', tags=['livro'])
aSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroPublic,
)
def create_livro(
    livro: LivroSchema,
    session: aSession,
    user: CurrentUser,
):
    search_livro = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )

    if search_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já consta no MADR',
        )

    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.id_romancista)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista não encontrado, insira a autoria primeiro',
        )

    db_livro = Livro(
        titulo=livro.titulo,
        ano=livro.ano,
        id_romancista=db_romancista.id,
    )

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)
    session.refresh(db_romancista)

    return db_livro


@router.get(
    '/{item_id}', status_code=HTTPStatus.OK, response_model=LivroPublic
)
def get_livro_by_id(
    item_id: int,
    user: CurrentUser,
    session: aSession,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == item_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    return db_livro


@router.get('/', status_code=HTTPStatus.OK, response_model=LivroList)
def get_livro_lista(  # noqa
    session: aSession,
    user: CurrentUser,
    titulo: str = Query(None),
    ano: int = Query(None),
    id_romancista: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Livro)

    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))

    if ano:
        query = query.filter(Livro.ano == ano)

    if id_romancista:
        query = query.filter(Livro.id_romancista == id_romancista)

    db_livros = session.scalars(query.offset(offset).limit(limit)).all()

    return {'livros': db_livros}


@router.patch('/{item_id}', response_model=LivroPublic)
def patch_livro(
    user: CurrentUser,
    item_id: int,
    session: aSession,
    livro: LivroUpdate,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == item_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    for key, value in livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)

    session.add(db_livro)
    session.commit()

    return db_livro


@router.delete('/{item_id}', response_model=Message)
def delete_livro(
    user: CurrentUser,
    item_id: int,
    session: aSession,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == item_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    session.delete(db_livro)
    session.commit()

    return {'message': 'Livro deletado no MADR'}
