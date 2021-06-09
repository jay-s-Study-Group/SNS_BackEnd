import requests
from unittest import TestCase
from fastapi.testclient import TestClient
from app.main import app


class TestUserAPI(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_update_user_successful(self):
        credentials = {
            "id": 2,
            "email": "hanbin8269@naver.com",
            "mentoring_field": "backend",
            "name": "hanbin",
            "self_introduction": "heelo, im hanbin",
            "phone_number": "01082693188",
            "profile_image": "s3.13224",
        }
        response = self.client.patch(f"/users/1", data=credentials)