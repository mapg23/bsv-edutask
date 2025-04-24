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


    def test_create_valid_user(self):

    def test_create_user_invalid_type(self):
    
    def test_create_user_invalid_duplicate(self):

    def test_create_user_missing_field(self):