import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from src.util.dao import DAO

from pymongo.errors import WriteError, DuplicateKeyError

class TestDAO:
    """
    Test for DAO.
    """

    @pytest.fixture
    def mock_dao(self):
        # Patch MongoClient so it doesn't actually connect to MongoDB
        with patch('src.util.dao.pymongo.MongoClient') as mock_mongo_client:
        # Create a fake collection and set up its behavior
            mock_collection = MagicMock()
            inserted_id = ObjectId()

            mock_collection.insert_one.return_value.inserted_id = inserted_id
            mock_collection.find_one.return_value = {
                '_id': inserted_id,
                'name': 'Mocked Name',
                'active': True
            }

            # Mock the database and collection access
            mock_db = MagicMock()
            mock_db.list_collection_names.return_value = ['testcollection']
            mock_db.__getitem__.return_value = mock_collection

            mock_mongo_client.return_value = MagicMock()
            mock_mongo_client.return_value.edutask = mock_db

            dao = DAO(collection_name='testcollection')

            return dao

    def test_create_valid_user(self, mock_dao):
        """
        Test with the right output
        """
        input_data = {'name': 'Mocked Name', 'active': True}

        result = mock_dao.create(input_data)

        assert result == {
            '_id' : result['_id'],
            'name': 'Mocked Name',
            'active': True
        }

    def test_create_user_invalid_type(self, mock_dao):
        """
        Tests wrong input type, bool instead of string.
        """

        invalid_data = {'name': False, 'active': 'Wrong'}

        mock_dao.collection.insert_one.side_effect = WriteError("Invalid type")
        
        with pytest.raises(WriteError):
            mock_dao.create(invalid_data)
    
    def test_create_user_invalid_duplicate(self,mock_dao):
        """
        Tests if the users input already exists in the database.
        """
        input_data = {'name': 'mocked name', 'active': True}

        mock_dao.collection.insert_one.side_effect = DuplicateKeyError("A duplicate key error occurred")

        with pytest.raises(DuplicateKeyError):
            mock_dao.create(input_data)

    def test_create_user_missing_field(self,mock_dao):
        """
        Tests if the users input does not contain all the required properties.
        """
        input_data = {'active': True}

        mock_dao.collection.insert_one.side_effect = WriteError("Field 'name' is required")

        with pytest.raises(WriteError):
            mock_dao.create(input_data)