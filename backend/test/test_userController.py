import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.controllers.usercontroller import UserController

import re

class TestUserController:
    """
    Test for user controller.
    """

    @pytest.fixture
    def mock_dao():
        return mock.MagicMock()

    @pytest.fixture
    def controller(mock_dao):
        return UserController(dao=mock_dao)

    def test_valid_email_and_user():
        ""
        ""

    def test_invalid_email_with_user():
        ""
        ""

    def test_valid_email_with_multiple_user():
        ""
        ""

    def test_valid_email_with_no_user():
        ""
        ""

    def test_invalid_email_and_user():
        ""
        ""