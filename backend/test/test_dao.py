import pytest
from unittest.mock import MagicMock

from src.util.dao import DAO

class TestUserController:
    """
    Test for user controller.
    """

    @pytest.fixture
    def mock_collection():
        collection = MagicMock()

        mock_inserted_id = ObjectId()

        collection.insert_one.return_value.inserted_id = mock_inserted_id