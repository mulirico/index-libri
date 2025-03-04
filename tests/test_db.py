from sqlalchemy import select

from index_libri.models import User


def test_create_user(session):
    new_user = User(
        username='alice', hashed_password='secret', email='teste@test'
    )
    session.add(new_user)

    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
