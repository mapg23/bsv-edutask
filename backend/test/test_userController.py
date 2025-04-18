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


