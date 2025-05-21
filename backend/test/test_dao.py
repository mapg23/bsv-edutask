import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from src.util.dao import DAO
from dotenv import load_dotenv

from pymongo.errors import WriteError, DuplicateKeyError

@pytest.mark.integration
class TestDAO:
    """
    Test for DAO.
    """

    @pytest.fixture(scope="function")
    def mock_dao(self, monkeypatch):
        load_dotenv()
        monkeypatch.setenv("MONGO_URL", "mongodb://root:root@localhost:27017")

        dao = DAO("user")
        dao.drop()
        dao = DAO("user")

        yield dao

        dao.drop()


    def test_create_valid_user(self, mock_dao):
        """
        Test with the right output
        """
        input_data = {'firstName': 'testFirstname', 'lastName' : 'testLastName', 'email': 'name@email.com'}

        result = mock_dao.create(input_data)

        assert result == {
            '_id' : result['_id'],
            'firstName': input_data['firstName'],
            'lastName': input_data['lastName'],
            'email': input_data['email']
        }

    def test_create_user_invalid_type(self, mock_dao):
        """
        Tests wrong input type, bool instead of string.
        """

        invalid_data = {'firstName': False, 'lastName': 10, 'email': None}

        with pytest.raises(WriteError):
            mock_dao.create(invalid_data)
    
    def test_create_user_invalid_duplicate(self,mock_dao):
        """
        Tests if the users input already exists in the database.
        """
        mock_dao.collection.create_index('email', unique=True)

        input_data = {'firstName': 'testFirstname', 'lastName' : 'testLastName', 'email': 'name@email.com'}

        # creates first entry of same data
        mock_dao.create(input_data)

        with pytest.raises(DuplicateKeyError):
            mock_dao.create(input_data)

    def test_create_user_missing_field(self,mock_dao):
        """
        Tests if the users input does not contain all the required properties.
        """
        input_data = {'firstName': 'testFirstname'}

        # mock_dao.collection.insert_one.side_effect = WriteError("Field 'name' is required")

        with pytest.raises(WriteError):
            mock_dao.create(input_data)
