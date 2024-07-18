import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from index_libri.app import app
from index_libri.database import get_session
from index_libri.models import Livro, Romancista, User, table_registry
from index_libri.security import get_password_hash


class ContaFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    hashed_password = factory.LazyAttribute(
        lambda obj: f'{obj.username}@example.com'
    )


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.sequence(lambda n: f'test{n}')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Faker('text')
    ano = factory.Faker('pyint', min_value=0, max_value=1000)
    id_romancista = factory.Faker('pyint', min_value=0, max_value=1000)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = 'testando'
    user = ContaFactory(hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = 'testando'

    return user


@pytest.fixture()
def other_user(session):
    password = 'testando2'
    user = ContaFactory(hashed_password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testando2'

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture()
def autora(session):
    autora = RomancistaFactory()
    session.add(autora)
    session.commit()
    session.refresh(autora)

    return autora


@pytest.fixture()
def livro(session):
    livro = LivroFactory()
    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro
