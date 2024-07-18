from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import Romancista, User
from index_libri.schemas import RomancistaPublic, RomancistaSchema
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
