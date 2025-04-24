import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from src.util.dao import DAO

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

            # Now create the DAO instance
            dao = DAO(collection_name='testcollection')

            return dao

    def test_create_valid_user(self, mock_dao):
        input_data = {'name': 'mocked name', 'active': True}

        result = mock_dao.create(input_data)

        assert result['name'].lower() == 'mocked name'
        assert result['active'] is True
        assert '_id' in result

    def test_create_user_invalid_type(self):
        pass
    
    def test_create_user_invalid_duplicate(self):
        pass

    def test_create_user_missing_field(self):
        pass