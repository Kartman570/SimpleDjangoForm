"""
Tests for viewsets.
Later we can divide this file into many, specific for each viewsets.
For now only UserViewset is present and tested.
"""
import django

django.setup()

import pytest
from rest_framework import status
from rest_framework.test import APIClient

import app.views.user as user_view_module


@pytest.fixture(autouse=True)
def clear_fake_db():
    """We must use the same fake DB variable as in the UserViewSet"""
    user_view_module.FAKE_DB.clear()
    user_view_module.NEXT_ID = 1


@pytest.fixture
def client():
    """Standard fixture to execute real HTTP requests"""
    return APIClient()


@pytest.fixture
def sample_user_data():
    """Sample data for test person"""
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
    """Sample data for another test person"""
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
    """
    Test class follows the structure:
    - CRUD operations testing (positive and main negative cases)
    - Exceptions and edgecases
    """
    def setUp(self):
        self.client = APIClient()

    # ___CREATE___
    @staticmethod
    def test_create_user(client, sample_user_data):
        """Check that we can create a new user and data properly saved"""
        resp = client.post("/users/", data=sample_user_data, format="json")
        body = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert body["id"] == 1
        assert body["firstname"] == sample_user_data["firstname"]
        assert len(user_view_module.FAKE_DB) == 1

    # ___LIST___
    @staticmethod
    def test_list_users_returns_all(client, sample_user_data, sample_user_data_second):
        """Check that we can retrieve list of all users (whether they are present or not)"""
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
        """Check that we can retrieve one specific user by its id"""
        client.post("/users/", data=sample_user_data, format="json")
        resp = client.get("/users/1/")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["firstname"] == sample_user_data["firstname"]

    @staticmethod
    def test_retrieve_not_found(client):
        """Check that we will get an error message if user does not exist"""
        resp = client.get("/users/999/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # ___PUT___
    @staticmethod
    def test_full_update_user_put(client, sample_user_data, sample_user_data_second):
        """Check that we can replace user data"""
        client.post("/users/", data=sample_user_data, format="json")
        resp = client.put("/users/1/", data=sample_user_data_second, format="json")

        del resp.json()["id"]
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == sample_user_data_second

    # ___PATCH___
    @staticmethod
    def test_partial_update_user_patch(client, sample_user_data, sample_user_data_second):
        """Check that we can update user data"""
        new_lastname = sample_user_data_second["lastname"]

        client.post("/users/", data=sample_user_data, format="json")
        resp = client.patch("/users/1/", data={"lastname": new_lastname}, format="json")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["lastname"] == new_lastname

    # ___DELETE___
    @staticmethod
    def test_delete_user(client, sample_user_data):
        """Check that we can delete user record"""
        client.post("/users/", data=sample_user_data, format="json")
        resp = client.delete("/users/1/")

        assert resp.status_code == status.HTTP_204_NO_CONTENT
        resp = client.get("/users/")
        assert len(resp.json()) == 0

    @staticmethod
    def test_delete_user_not_found(client):
        """Check that we will get an error trying to delete user that does not exist"""
        resp = client.delete("/users/999/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # ___VALIDATION___
    @staticmethod
    def test_create_user_incorrect_firstname(client, sample_user_data):
        """User form requirement - firstname length limited by 10 characters"""
        new_data = {**sample_user_data, "firstname": "JohnJohnJo"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "firstname": "JohnJohnJoh"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @staticmethod
    def test_create_user_incorrect_lastname(client, sample_user_data):
        """User form requirement - lastname length limited by 20 characters"""
        new_data = {**sample_user_data, "lastname": "Doedoedoedoedoedoedo"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "lastname": "Doedoedoedoedoedoedoe"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @staticmethod
    def test_create_user_incorrect_email(client, sample_user_data):
        """User form requirement - email must be valid address"""
        new_data = {**sample_user_data, "email": "John@example.com"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "email": "John@example"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        new_data = {**sample_user_data, "email": "John.com"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        new_data = {**sample_user_data, "email": "John@com"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @staticmethod
    def test_create_user_incorrect_exp(client, sample_user_data):
        """User form requirement - experience must be choice"""
        new_data = {**sample_user_data, "experience": "low"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "experience": "medium"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "experience": "high"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        new_data = {**sample_user_data, "experience": "some_level"}
        resp = client.post("/users/", data=new_data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
