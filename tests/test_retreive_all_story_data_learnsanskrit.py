import pytest
from unittest.mock import patch

from services.learnsanskrit_metadata_services import RetrieveAllStoryDataLearnSanskrit


# =========================================================
# SUCCESS CASE
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_all_success(mock_repo):

    mock_data = [
        {
            "_id": "1",
            "title": "Rabbit Story"
        }
    ]

    mock_repo.return_value.get_all.return_value = mock_data

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert result["success"] is True
    assert result["data"] == mock_data
    assert len(result["data"]) == 1
    assert result["data"][0]["title"] == "Rabbit Story"


# =========================================================
# EMPTY LIST
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_all_empty_list(mock_repo):

    mock_repo.return_value.get_all.return_value = []

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert result["success"] is True
    assert result["data"] == []


# =========================================================
# NONE RESPONSE
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_all_none_response(mock_repo):

    mock_repo.return_value.get_all.return_value = None

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert result["success"] is True
    assert result["data"] is None



# =========================================================
# GENERIC EXCEPTION
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_all_generic_exception(mock_repo):

    mock_repo.return_value.get_all.side_effect = Exception(
        "Unexpected Error"
    )

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert result["success"] is False
    assert result["message"] == "Unexpected Error"


# =========================================================
# RESPONSE STRUCTURE
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_all_response_structure(mock_repo):

    mock_repo.return_value.get_all.return_value = []

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert isinstance(result, dict)
    assert "success" in result
    assert "data" in result


# =========================================================
# VERIFY REPOSITORY METHOD CALLED
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_repository_method_called_once(mock_repo):

    mock_repo.return_value.get_all.return_value = []

    service = RetrieveAllStoryDataLearnSanskrit()

    service.retrieve_all()

    mock_repo.return_value.get_all.assert_called_once()


# =========================================================
# LARGE DATASET
# =========================================================

@patch(
    "services.learnsanskrit_metadata_services.GetUnusedStories"
)
def test_retrieve_large_dataset(mock_repo):

    mock_data = [
        {
            "_id": str(i),
            "title": f"Story {i}"
        }
        for i in range(1000)
    ]

    mock_repo.return_value.get_all.return_value = mock_data

    service = RetrieveAllStoryDataLearnSanskrit()

    result = service.retrieve_all()

    assert result["success"] is True
    assert len(result["data"]) == 1000
    assert result["data"][500]["title"] == "Story 500"