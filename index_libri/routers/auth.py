from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from index_libri.database import get_session
from index_libri.models import User
from index_libri.schemas import Token
from index_libri.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
aSession = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2Form,
    session: aSession,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
