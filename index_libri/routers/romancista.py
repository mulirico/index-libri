from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import Romancista, User
from index_libri.schemas import (
    Message,
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
    RomancistaUpdate,
)
from index_libri.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancista'])
aSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaPublic,
)
def create_romancista(
    romancista: RomancistaSchema,
    session: aSession,
    user: CurrentUser,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista já consta no MADR',
        )

    db_romancista = Romancista(nome=romancista.nome)
    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.get(
    '/{item_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaPublic,
)
def get_romancista_id(
    item_id: int,
    session: aSession,
    user: CurrentUser,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == item_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    return db_romancista


@router.get('/', response_model=RomancistaList, status_code=HTTPStatus.OK)
def get_romancista_lista(
    session: aSession,
    user: CurrentUser,
    nome: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Romancista)

    if nome:
        query = query.filter(Romancista.nome.contains(nome))

    romancistas = session.scalars(query.offset(offset).limit(limit)).all()

    return {'romancistas': romancistas}


@router.patch('/{item_id}', response_model=RomancistaPublic)
def patch_romancista(
    item_id: int,
    user: CurrentUser,
    session: aSession,
    romancista: RomancistaUpdate,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == item_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    for key, value in romancista.model_dump(exclude_unset=True).items():
        setattr(db_romancista, key, value)

    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.delete('/{item_id}', response_model=Message)
def delete_romancista(
    item_id: int,
    user: CurrentUser,
    session: aSession,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == item_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_romancista)
    session.commit()

    return {'message': 'Romancista deletada no MADR'}
