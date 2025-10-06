import django

django.setup()

import pytest
from rest_framework import status
from rest_framework.test import APIClient

# for mocking DB
import app.views.user as user_view_module


@pytest.fixture(autouse=True)
def clear_fake_db():
    user_view_module.FAKE_DB.clear()
    user_view_module.NEXT_ID = 1


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_user_data():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "John@example.com",
        "country": "USA",
        "code": "111",
        "phone": "123456789",
        "experience": "low",
    }

@pytest.fixture
def sample_user_data_second():
    return {
        "firstname": "Jane",
        "lastname": "Doe2",
        "email": "Jane@example.com",
        "country": "USA",
        "code": "111",
        "phone": "123456789",
        "experience": "low",
    }

class TestUserView:
    def setUp(self):
        self.client = APIClient()

    # ___CREATE___
    @staticmethod
    def test_create_user(client, sample_user_data):
        resp = client.post("/users/", data=sample_user_data, format="json")
        body = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert body["id"] == 1
        assert body["firstname"] == sample_user_data["firstname"]
        assert len(user_view_module.FAKE_DB) == 1

    # ___LIST___
    @staticmethod
    def test_list_users_returns_all(client, sample_user_data, sample_user_data_second):
        resp = client.get("/users/")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == 0

        client.post("/users/", data=sample_user_data, format="json")
        client.post("/users/", data=sample_user_data_second, format="json")

        resp = client.get("/users/")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["firstname"] == sample_user_data["firstname"]
        assert data[1]["firstname"] == sample_user_data_second["firstname"]

    # ___RETRIEVE___
    @staticmethod
    def test_retrieve_user_by_id(client, sample_user_data):
        client.post("/users/", data=sample_user_data, format="json")
        resp = client.get("/users/1/")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["firstname"] == sample_user_data["firstname"]

    @staticmethod
    def test_retrieve_not_found(client):
        resp = client.get("/users/999/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # ___PUT___
    @staticmethod
    def test_full_update_user_put(client, sample_user_data, sample_user_data_second):
        new_data = {**sample_user_data, "firstname": sample_user_data_second["firstname"]}

        client.post("/users/", data=sample_user_data, format="json")
        resp = client.put("/users/1/", data=new_data, format="json")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["firstname"] == sample_user_data_second["firstname"]

    # ___PATCH___
    @staticmethod
    def test_partial_update_user_patch(client, sample_user_data, sample_user_data_second):
        new_lastname = sample_user_data_second["lastname"]

        client.post("/users/", data=sample_user_data, format="json")
        resp = client.patch("/users/1/", data={"lastname": new_lastname}, format="json")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["lastname"] == new_lastname

    # ___DELETE___
    @staticmethod
    def test_delete_user(client, sample_user_data):
        client.post("/users/", data=sample_user_data, format="json")
        resp = client.delete("/users/1/")

        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert len(user_view_module.FAKE_DB) == 0

    @staticmethod
    def test_delete_user_not_found(client):
        resp = client.delete("/users/999/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # ___VALIDATION___
    @staticmethod
    def test_create_user_incorrect_name(client, sample_user_data):
        new_data = {**sample_user_data, "firstname": "JohnJohnJohnJohnJohn"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @staticmethod
    def test_create_user_incorrect_email(client, sample_user_data):
        new_data = {**sample_user_data, "email": "John@example"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @staticmethod
    def test_create_user_incorrect_exp(client, sample_user_data):
        new_data = {**sample_user_data, "experience": "some_level"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
