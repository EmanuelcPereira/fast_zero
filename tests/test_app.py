from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.schemas import UserPublic


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'John Doe',
            'email': 'john_doe@mail.com',
            'password': '2345678',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'John Doe',
        'email': 'john_doe@mail.com',
        'id': 1,
    }


def test_create_user_with_username_already_exists(client):
    client.post(
        '/users',
        json={
            'username': 'Severino',
            'email': 'severino_felix@mail.com',
            'password': 'tanahorademolharobiscoito',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'Severino',
            'email': 'john_doe@mail.com',
            'password': '2345678',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_email_already_exists(client):
    client.post(
        '/users',
        json={
            'username': 'Severino',
            'email': 'severino_felix@mail.com',
            'password': 'tanahorademolharobiscoito',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'Juvenal',
            'email': 'severino_felix@mail.com',
            'password': '2345678',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    client.post(
        '/users',
        json={
            'username': 'Severino',
            'email': 'severino_felix@mail.com',
            'password': 'tanahorademolharobiscoito',
        },
    )

    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'John Doe',
        'email': 'john_doe@mail.com',
        'id': 1,
    }


def test_read_user_error(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bob Doe',
            'email': 'bob_doe@mail.com',
            'password': 'ta na hora de molhar o biscoite',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob Doe',
        'email': 'bob_doe@mail.com',
        'id': 1,
    }


def test_update_user_error(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'Bob Doe',
            'email': 'bob_doe@mail.com',
            'password': 'ta na hora de molhar o biscoite',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'Severino',
            'email': 'severino_felix@mail.com',
            'password': 'tanahorademolharobiscoito',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'Severino',
            'email': 'bob_dylan@mail.com',
            'password': '2345678',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user):
    client.post(
        '/users',
        json={
            'username': 'Severino',
            'email': 'severino_felix@mail.com',
            'password': 'tanahorademolharobiscoito',
        },
    )

    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_error(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
