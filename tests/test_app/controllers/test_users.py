from app.controllers.users import UserController
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch


class TestUserController(TestCase):
    @patch("app.models.users.User.update")
    def test_update_user(self, mock_user_update):
        credentials = {
            "mentoring_field": "backend",
            "name": "hanbin",
            "self_introduction": "heelo, im hanbin",
            "phone_number": "01082693188",
            "profile_image": "s3.13224",
        }
        UserController().update_user(1, **credentials)
