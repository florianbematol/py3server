import pytest
import requests


@pytest.mark.run(order=1)
def test_users_api_create_user():
    # GIVEN
    url: str = 'http://localhost:8080/users'
    user_data: object = {
        'firstname': 'user1_firstname',
        'lastname': 'user1_lastname',
    }

    # WHEN
    res: requests.Response = requests.post(url, json=user_data)

    # THEN
    assert res.status_code == 200
    assert res.json() == {
        'firstname': 'user1_firstname',
        'lastname': 'user1_lastname',
        'age': 0
    }


@pytest.mark.run(order=2)
def test_users_api_create_user_with_age():
    # GIVEN
    url: str = 'http://localhost:8080/users'
    user_data: object = {
        'firstname': 'user2_firstname',
        'lastname': 'user2_lastname',
        'age': 25
    }

    # WHEN
    res: requests.Response = requests.post(url, json=user_data)

    # THEN
    assert res.status_code == 200
    assert res.json() == {
        'firstname': 'user2_firstname',
        'lastname': 'user2_lastname',
        'age': 25
    }


@pytest.mark.run(order=3)
def test_users_api_get_all_users():
    # GIVEN
    url: str = 'http://localhost:8080/users'

    # WHEN
    res: requests.Response = requests.get(url)

    # THEN
    assert res.status_code == 200
    assert res.json() == [
        {
            'firstname': 'user1_firstname',
            'lastname': 'user1_lastname',
            'age': 0
        },
        {
            'firstname': 'user2_firstname',
            'lastname': 'user2_lastname',
            'age': 25
        }
    ]


@pytest.mark.run(order=4)
def test_users_api_get_user_2():
    # GIVEN
    url: str = 'http://localhost:8080/users/2'

    # WHEN
    res: requests.Response = requests.get(url)

    # THEN
    assert res.status_code == 200
    assert res.json() == {
        'firstname': 'user2_firstname',
        'lastname': 'user2_lastname',
        'age': 25
    }


@pytest.mark.run(order=5)
def test_users_api_update_user_2():
    # GIVEN
    url: str = 'http://localhost:8080/users/2'
    data: object = {
        'firstname': 'user2_updated_firstname'
    }

    # WHEN
    res: requests.Response = requests.put(url, json=data)

    # THEN
    assert res.status_code == 200
    assert res.json() == {
        'firstname': 'user2_updated_firstname',
        'lastname': 'user2_lastname',
        'age': 25
    }


@pytest.mark.run(order=6)
def test_users_api_delete_user_2():
    # GIVEN
    url: str = 'http://localhost:8080/users/2'

    # WHEN
    res: requests.Response = requests.delete(url)

    # THEN
    assert res.status_code == 204
