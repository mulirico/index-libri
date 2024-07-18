from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import Livro, Romancista, User
from index_libri.schemas import LivroPublic, LivroSchema
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
