from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Emanuel', email='emanuel@mail.com', password='2345678'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'emanuel@mail.com')
    )

    assert result.username == 'Emanuel'
