from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Peter Parker',
        password='porco aranha',
        email='miranha@test.com',
    )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'miranha@test.com')
    )

    assert result.username == 'Peter Parker'
