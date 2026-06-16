import pytest
from unittest.mock import patch

from services.tokenized_data_service import RetrieveTokenizedStoryById


class TestRetrieveTokenizedStoryById:
    
# =========================================================
# When No Story Id
# =========================================================

    def test_raises_value_error_when_story_id_is_none(self):

        with pytest.raises(ValueError) as exc:

            RetrieveTokenizedStoryById(None)

        assert str(exc.value) == "story_id cannot be None"
        
        
# =========================================================
# SUCCESS CASE
# =========================================================

@patch("services.tokenized_data_service.GetTokenizedStoryByIdFromMongoDB")
def test_returns_story_when_story_exists(mock_repository):

    mock_repository.return_value.get_story.return_value = {
        "_id": "1",
        "title": "Lion and Mouse"
    }

    service = RetrieveTokenizedStoryById("1")
    result = service.retrieve_story()

    assert result == {
        "_id": "1",
        "title": "Lion and Mouse"
    }
        
# =========================================================
# Repository Called with correct id
# =========================================================
@patch("services.tokenized_data_service.GetTokenizedStoryByIdFromMongoDB")
def test_repository_called_with_correct_story_id(mock_repository):

    mock_repository.return_value.get_story.return_value = {"_id": "1"}

    service = RetrieveTokenizedStoryById("1")
    service.retrieve_story()

    mock_repository.assert_called_once_with("1")
    
# =========================================================
# Repository Called only once
# =========================================================

    @patch(
        "services.tokenized_data_service.GetTokenizedStoryById"
    )
    def test_repository_retrieve_story_called_once(
        self,
        mock_repository
    ):

        mock_repository.return_value.retrieve_story.return_value = {
            "_id": "1"
        }

        service = RetrieveTokenizedStoryById("1")

        service.retrieve_story()

        mock_repository.return_value.retrieve_story.assert_called_once()
        
# =========================================================
# Database error
# =========================================================

@patch("services.tokenized_data_service.GetTokenizedStoryByIdFromMongoDB")
def test_propagates_repository_exceptions(mock_repository):

    mock_repository.return_value.get_story.side_effect = Exception("Database error")

    service = RetrieveTokenizedStoryById("1")

    with pytest.raises(Exception) as exc:
        service.retrieve_story()

    assert str(exc.value) == "Database error"