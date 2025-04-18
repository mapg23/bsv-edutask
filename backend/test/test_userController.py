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

    def test_valid_email_and_user(self, mock_dao, controller):
        """"
        Test with exactly one user and a valid email address.
        """
        email = "user@example.com"
        mock_user = {"email": email, "name": "User"}
        mock_dao.find.return_value = [mock_user]

        try:
            result = controller.get_user_by_email(email)

            mock_dao.find.assert_called_once_with({'email': email})

            assert result == mock_user
        except Exception as e:
            pytest.fail(f"Testet misslyckades med ett oväntat fel: {e}")

    def test_invalid_email_with_user(self, controller, mock_dao):
        """
        Test with an invalid email address.
        """
        invalid_email = "not-an-email"

        with pytest.raises(ValueError, match="invalid email address"):
            controller.get_user_by_email(invalid_email)

        mock_dao.find.assert_not_called()

    def test_valid_email_with_multiple_user(self, capsys, mock_dao, controller):
        """
        Test with multiple users and a valid email address.
        """
        email = "duplicate@example.com"
        user1 = {"email": email, "name": "User1"}
        user2 = {"email": email, "name": "User2"}
        mock_dao.find.return_value = [user1, user2]

        result = controller.get_user_by_email(email)
        captured = capsys.readouterr()

        assert result == user1
        assert f"more than one user found with mail {email}" in captured.out

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