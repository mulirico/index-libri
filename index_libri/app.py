from http import HTTPStatus

from fastapi import FastAPI

from index_libri.routers import contas
from index_libri.schemas import Message

app = FastAPI()

app.include_router(contas.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'index libri api'}
