from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import User
from index_libri.schemas import ContaPublic, ContaSchema

router = APIRouter(prefix='/contas', tags=['contas'])


# @router.post('/', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
# def create_conta(conta: ContaSchema, session: Session = Depends(get_session)):
#     db_user = session.scalar(
#         select(User).where(User.username == conta.username)
#     )
#     if db_user:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail='Username já registrado',
#         )
#     fake_hashed_password = conta.password + 'fakehashed'
#     db_user = User(
#         username=conta.username,
#         email=conta.email,
#         hashed_password=fake_hashed_password,
#     )
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)

#     return db_user


# @router.get('/', response_model=ContaList)
# def read_contas():
#     return {'contas': database}


# @router.get('/contas/{id}', response_model=ContaList)
# def read_contas_with_id():


# @router.put('/{conta_id}', response_model=ContaPublic)
# def update_conta(conta_id: int, conta: ContaSchema):
#     if conta_id > len(database) or conta_id < 1:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

#     conta_with_id = ContaDB(**conta.model_dump(), id=conta_id)
#     database[conta_id - 1] = conta_with_id

#     return conta_with_id


# @router.delete('/{conta_id}', response_model=Message)
# def delete_conta(conta_id: int):
#     if conta_id > len(database) or conta_id < 1:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

#     del database[conta_id - 1]

#     return {'message': 'Conta deletada com sucesso'}
