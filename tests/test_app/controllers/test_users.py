from app.controllers.users import UserController
from unittest import TestCase
from unittest.mock import patch
from fastapi import HTTPException


class TestUserController(TestCase):
    @patch("app.models.users.User.update")
    @patch("app.models.users.MentoringField.filter")
    def test_update_user_successful(
        self, mock_user_update, mock_mentoring_field_filter
    ):
        credentials = {
            "mentoring_fields": ["backend"],
            "name": "hanbin",
            "self_introduction": "heelo, im hanbin",
            "phone_number": "01082693188",
            "profile_image": "s3.13224",
        }
        mock_user_update.where().return_value = credentials
        mock_mentoring_field_filter.first().return_value = "backend"
        try:
            user_instance = UserController().update_user(1, **credentials)
        except HTTPException as exe:
            self.fail(exe.detail)