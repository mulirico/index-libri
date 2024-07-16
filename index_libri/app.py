from http import HTTPStatus

from fastapi import FastAPI

from index_libri.routers import auth, contas, romancista
from index_libri.schemas import Message

app = FastAPI()

app.include_router(contas.router)
app.include_router(auth.router)
app.include_router(romancista.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'index libri api'}
