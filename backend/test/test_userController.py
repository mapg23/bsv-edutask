import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

import re


class TestUserController:
    """
    Test for user controller.
    """

    @pytest.fixture
    def mock_dao(self):
        return MagicMock()

    @pytest.fixture
    def controller(self, mock_dao):
        return UserController(dao=mock_dao)

    def test_valid_email_and_user(self):
        ""
        ""

    def test_invalid_email_with_user(self):
        ""
        ""

    def test_valid_email_with_multiple_user(self):
        ""
        ""

    def test_valid_email_with_no_user(self, controller, mock_dao):
        email = 'username@email.com'

        mock_dao.find.return_value = []

        try:
            user = controller.get_user_by_email(email)
        except IndexError as index_error_msg:
            assert str(index_error_msg) == 'list index out of range'

        mock_dao.find.assert_called_once_with({'email': email})

    def test_invalid_email_and_user(self, controller):
        email = 'invalid'
        try:
            controller.get_user_by_email(email)
        except ValueError as error_msg:
            assert str(error_msg) == 'Error: invalid email address'