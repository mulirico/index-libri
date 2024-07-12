from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import User
from index_libri.schemas import ContaList, ContaPublic, ContaSchema, Message
from index_libri.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/contas', tags=['contas'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def create_conta(conta: ContaSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == conta.username) | (User.email == conta.email)
        )
    )
    if db_user:
        if db_user.username == conta.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username já registrado',
            )
        elif db_user.email == conta.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já registrado',
            )
    hash_password = get_password_hash(conta.password)
    db_user = User(
        username=conta.username,
        email=conta.email,
        hashed_password=hash_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=ContaList)
def read_contas(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'contas': users}


# @router.get(
#     '/{id}', response_model=ContaList, status_code=HTTPStatus.OK
# )
# def read_contas_with_id(
#     id: int, conta: ContaPublic, session: Session = Depends(get_session)
# ):
#     user = session.scalar(select(User).where(conta.id == id))
#     if not user:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
#         )

#     return {'conta': user}


@router.put('/{conta_id}', response_model=ContaPublic)
def update_conta(
    conta_id: int,
    conta: ContaSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Não autorizado',
        )

    current_user.username = conta.username
    current_user.email = conta.email
    current_user.hashed_password = get_password_hash(conta.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{conta_id}', response_model=Message)
def delete_conta(
    conta_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Não autorizado',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
