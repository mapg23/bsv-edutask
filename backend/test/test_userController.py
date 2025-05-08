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

        result = controller.get_user_by_email(email)

        mock_dao.find.assert_called_once_with({'email': email})
        assert result == mock_user

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
        """
        Tests with valid email and no users.
        """
        email = 'username@email.com'

        mock_dao.find.return_value = []

        with pytest.raises(IndexError, match="list index out of range"):
            controller.get_user_by_email(email)

        mock_dao.find.assert_called_once_with({'email': email})


    def test_invalid_email_and_user(self, controller,mock_dao):
        """
        Tests with invalid email and one user.
        """
        email = 'invalid'

        with pytest.raises(ValueError, match="invalid email address"):
            controller.get_user_by_email(email)

        mock_dao.find.assert_not_called()