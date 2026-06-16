from unittest.mock import patch
from services.tokenized_data_service import RetrieveTokenizedStories

# =========================================================
# SUCCESS CASE
# =========================================================

@patch("services.tokenized_data_service.GetAllTokenizedStoriesFromMongoDB")
def test_get_all_success(mock_repo):

    mock_data = [
        {"_id": "1", "title": "Rabbit Story"}
    ]

    mock_repo.return_value.get_all.return_value = {
        "success": True,
        "count": 1,
        "data": mock_data
    }

    service = RetrieveTokenizedStories()
    result = service.get_all()

    assert result["success"] is True
    assert result["data"] == mock_data
    
    
# =========================================================
# EMPTY LIST
# =========================================================
@patch("services.tokenized_data_service.GetAllTokenizedStoriesFromMongoDB")
def test_get_all_empty_data(mock_repo):

    mock_repo.return_value.get_all.return_value = {
        "success": True,
        "count": 0,
        "data": []
    }

    service = RetrieveTokenizedStories()
    result = service.get_all()

    assert result["success"] is True
    assert result["data"] == []
    
# =========================================================
# FIle Not Found
# =========================================================
@patch("services.tokenized_data_service.GetAllTokenizedStoriesFromMongoDB")
def test_get_all_file_not_found(mock_repo):

    mock_repo.return_value.get_all.side_effect = FileNotFoundError(
        "tokenized_stories.json not found"
    )

    service = RetrieveTokenizedStories()
    result = service.get_all()

    assert result["success"] is False
    assert "not found" in result["message"]
    
# =========================================================
# Unexpected Exception
# =========================================================

@patch("services.tokenized_data_service.GetAllTokenizedStoriesFromMongoDB")
def test_get_all_unexpected_exception(mock_repo):

    mock_repo.return_value.get_all.side_effect = Exception("Unexpected Error")

    service = RetrieveTokenizedStories()
    result = service.get_all()

    assert result["success"] is False
    assert result["message"] == "Unexpected Error"
    
    


