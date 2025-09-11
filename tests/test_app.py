from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'John Doe',
            'password': 'passwd',
            'email': 'john.doe@mail.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'john.doe@mail.com',
        'id': 1,
        'username': 'John Doe',
    }


def test_create_user_username_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'jonh.doe2@mail.com',
            'password': 'newPasswd',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'John Doe Secont',
            'email': user.email,
            'password': 'newPasswd',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user_error(client, user):
    response = client.put(
        'users/10',
        json={
            'username': 'Jane Doe',
            'email': 'jane_doe@mail.com',
            'id': 1,
            'password': 'passwd',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    body = response.json()
    assert body['detail'] == 'User not found'


def test_update_user(client, user):
    response = client.put(
        'users/1',
        json={
            'username': 'Jane Doe',
            'email': 'jane_doe@mail.com',
            'id': 1,
            'password': 'passwd',
        },
    )

    assert response.json() == {
        'username': 'Jane Doe',
        'email': 'jane_doe@mail.com',
        'id': 1,
    }


def test_delete_user_error(client, user):
    response = client.delete('users/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
