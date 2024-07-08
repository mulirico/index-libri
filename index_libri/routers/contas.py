from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from index_libri.schemas import (
    ContaDB,
    ContaList,
    ContaPublic,
    ContaSchema,
    Message,
)

router = APIRouter(prefix='/contas', tags=['contas'])

database = []


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def create_conta(conta: ContaSchema):
    conta_with_id = ContaDB(**conta.model_dump(), id=len(database) + 1)

    database.append(conta_with_id)

    return conta_with_id


@router.get('/', response_model=ContaList)
def read_contas():
    return {'contas': database}


# @router.get('/contas/{id}', response_model=ContaList)
# def read_contas_with_id():


@router.put('/{conta_id}', response_model=ContaPublic)
def update_conta(conta_id: int, conta: ContaSchema):
    if conta_id > len(database) or conta_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    conta_with_id = ContaDB(**conta.model_dump(), id=conta_id)
    database[conta_id - 1] = conta_with_id

    return conta_with_id


@router.delete('/{conta_id}', response_model=Message)
def delete_conta(conta_id: int):
    if conta_id > len(database) or conta_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    del database[conta_id - 1]

    return {'message': 'Conta deletada com sucesso'}
