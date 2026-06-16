from unittest.mock import patch, MagicMock

from repository.tokenized_data_repo import GetAllTokenizedStoriesFromMongoDB


@patch("repository.tokenized_data_repo.connect_db")
def test_get_all_stories_success(mock_connect_db):

    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {
            "_id": "1",
            "title": "Rabbit Story"
        }
    ]

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    mock_connect_db.return_value = mock_db

    repo = GetAllTokenizedStoriesFromMongoDB()

    result = repo.get_all()

    assert result["success"] is True
    assert result["count"] == 1
    assert len(result["data"]) == 1
    assert result["data"][0]["title"] == "Rabbit Story"