from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'john.doe@mail.com',
                'id': 1,
                'username': 'John Doe',
            }
        ]
    }


def test_update_user_error(client):
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
    assert body['detail'] == 'User Not Found'


def test_update_user(client):
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


def test_delete_user_error(client):
    response = client.delete('users/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
