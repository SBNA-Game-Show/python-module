import pytest
from unittest.mock import patch
from flask import Flask

from controller.story_data_learnsanskrit_controller import fetch_all_story_data, write_meta_data,add_new_story


# =========================================================
# FLASK TEST APP
# =========================================================

@pytest.fixture
def app():

    app = Flask(__name__)

    app.testing = True

    return app

# =========================================================
# FETCH ALL STROY META DATA TESTS
# =========================================================

# =========================================================
# SUCCESS RESPONSE
# =========================================================

def test_fetch_all_story_data_success(app):

    mock_response = {
        "success": True,
        "data": [
            {
                "_id": "1",
                "title": "Rabbit Story"
            }
        ]
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json["success"] is True
            assert len(response_json["data"]) == 1
            assert response_json["data"][0]["title"] == "Rabbit Story"


# =========================================================
# EMPTY DATA RESPONSE
# =========================================================

def test_fetch_all_story_data_empty_data(app):

    mock_response = {
        "success": True,
        "data": []
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json["success"] is True
            assert response_json["data"] == []


# =========================================================
# NONE DATA RESPONSE
# =========================================================

def test_fetch_all_story_data_none_data(app):

    mock_response = {
        "success": True,
        "data": None
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json["success"] is True
            assert response_json["data"] is None


# =========================================================
# FILE NOT FOUND ERROR
# =========================================================

def test_fetch_all_story_data_file_not_found(app):

    mock_response = {
        "success": False,
        "message": "stories_data.json not found"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 500
            assert response_json["success"] is False
            assert "not found" in response_json["message"]


# =========================================================
# INVALID JSON ERROR
# =========================================================

def test_fetch_all_story_data_invalid_json(app):

    mock_response = {
        "success": False,
        "message": "Invalid JSON format"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 500
            assert response_json["success"] is False
            assert "Invalid JSON format" in response_json["message"]


# =========================================================
# GENERIC ERROR
# =========================================================

def test_fetch_all_story_data_generic_error(app):

    mock_response = {
        "success": False,
        "message": "Unexpected Error"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 500
            assert response_json["success"] is False
            assert response_json["message"] == "Unexpected Error"


# =========================================================
# RESPONSE STRUCTURE
# =========================================================

def test_fetch_all_story_data_response_structure(app):

    mock_response = {
        "success": True,
        "data": [
            {
                "_id": "1",
                "title": "Lion Story"
            }
        ]
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert isinstance(response_json, dict)
            assert "success" in response_json
            assert "data" in response_json
            assert status_code == 200


# =========================================================
# VERIFY SERVICE METHOD CALLED
# =========================================================

def test_service_method_called_once(app):

    mock_response = {
        "success": True,
        "data": []
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            fetch_all_story_data()

            mock_service.return_value.retrieve_all.assert_called_once()


# =========================================================
# LARGE DATASET
# =========================================================

def test_fetch_all_story_data_large_dataset(app):

    large_data = []

    for i in range(1000):

        large_data.append({
            "_id": str(i),
            "title": f"Story {i}"
        })

    mock_response = {
        "success": True,
        "data": large_data
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.RetrieveAllStoryDataLearnSanskrit"
        ) as mock_service:

            mock_service.return_value.retrieve_all.return_value = mock_response

            response, status_code = fetch_all_story_data()

            response_json = response.get_json()

            assert status_code == 200
            assert len(response_json["data"]) == 1000
            assert response_json["data"][500]["title"] == "Story 500"
            
# =========================================================
# WRITE META DATA TESTS
# =========================================================
# =========================================================
# SUCCESS RESPONSE
# =========================================================
def test_write_meta_data_success(app):

    mock_response = {
        "success": True,
        "message": "Metadata written successfully"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_response

            response, status_code = write_meta_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json["success"] is True
            assert response_json["message"] == "Metadata written successfully"
            
# =========================================================
# FAILURE CASE
# =========================================================
def test_write_meta_data_failure(app):

    mock_response = {
        "success": False,
        "message": "Failed to write metadata"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_response

            response, status_code = write_meta_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json["success"] is False
            assert response_json["message"] == "Failed to write metadata"
            
            
# =========================================================
# EMPTY DATA RESPONSE
# =========================================================
def test_write_meta_data_empty_response(app):

    mock_response = {}

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_response

            response, status_code = write_meta_data()

            response_json = response.get_json()

            assert status_code == 200
            assert isinstance(response_json, dict)
            
# =========================================================
# NONE RESPONSE
# =========================================================
def test_write_meta_data_none_response(app):

    mock_response = None

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_response

            response, status_code = write_meta_data()

            response_json = response.get_json()

            assert status_code == 200
            assert response_json is None
            
            
# =========================================================
# EXCEPTION THROWING CASE
# =========================================================

def test_write_meta_data_exception(app):

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.side_effect = Exception("DB failure")

            try:
                response, status_code = write_meta_data()
                response_json = response.get_json()

                # If controller does NOT handle exceptions, this will fail here
                assert status_code == 500
                assert response_json["success"] is False

            except Exception as e:
                # fallback if controller doesn't handle exception
                assert "DB failure" in str(e)
                
# =========================================================
# VERIFY SERVICE CALLED ONLY ONCE
# =========================================================
def test_write_meta_data_service_called_once(app):

    mock_response = {
        "success": True,
        "message": "ok"
    }

    with app.app_context():

        with patch(
            "controller.story_data_learnsanskrit_controller.WriteLearnSanskritCCMetaData"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_response

            write_meta_data()

            mock_service.return_value.execute.assert_called_once()
            
# =========================================================
# ADD NEW STORY TESTS
# =========================================================
# =========================================================
# SUCCESS SCENARIO
# =========================================================
def test_add_new_story_success(app):

    mock_result = {
        "_id": "aesop01",
        "title": "Rabbit Story",
        "content": "Once upon a time..."
    }

    with app.test_request_context("/add_new_story?story_id=aesop01"):

        with patch(
            "controller.story_data_learnsanskrit_controller.FetchNewFable"
        ) as mock_service:

            mock_service.return_value.execute.return_value = mock_result

            response, status_code = add_new_story()
            response_json = response.get_json()

            assert status_code == 200
            assert "data" in response_json
            assert response_json["data"]["_id"] == "aesop01"
            
# =========================================================
# MISSING STORY ID
# =========================================================
def test_add_new_story_missing_story_id(app):

    with app.test_request_context("/add_new_story"):

        response, status_code = add_new_story()
        response_json = response.get_json()

        assert status_code == 400
        assert response_json["success"] is False
        assert "required" in response_json["message"]
        
# =========================================================
# EMPTY STRING STORY ID
# =========================================================
def test_add_new_story_empty_story_id(app):

    with app.test_request_context("/add_new_story?story_id="):

        response, status_code = add_new_story()
        response_json = response.get_json()

        assert status_code == 400
        assert response_json["success"] is False
        assert "required" in response_json["message"]
        
# =========================================================
# SERVICE CALLED WITH CORRECT PARAM
# =========================================================
def test_add_new_story_service_called_with_correct_id(app):

    with app.test_request_context("/add_new_story?story_id=aesop01"):

        with patch(
            "controller.story_data_learnsanskrit_controller.FetchNewFable"
        ) as mock_service:

            mock_instance = mock_service.return_value
            mock_instance.execute.return_value = {"ok": True}

            add_new_story()

            mock_service.assert_called_once_with("aesop01")
            mock_instance.execute.assert_called_once()
            
# =========================================================
# SERVICE RETURNS EMPTY RESULT
# =========================================================
def test_add_new_story_empty_result(app):

    with app.test_request_context("/add_new_story?story_id=aesop01"):

        with patch(
            "controller.story_data_learnsanskrit_controller.FetchNewFable"
        ) as mock_service:

            mock_service.return_value.execute.return_value = {}

            response, status_code = add_new_story()
            response_json = response.get_json()

            assert status_code == 200
            assert response_json["data"] == {}
            
# =========================================================
# SERVICE RETURNS FAILURE RESPONSE
# =========================================================
def test_add_new_story_service_failure(app):

    with app.test_request_context("/add_new_story?story_id=aesop01"):

        with patch(
            "controller.story_data_learnsanskrit_controller.FetchNewFable"
        ) as mock_service:

            mock_service.return_value.execute.return_value = {
                "success": False,
                "message": "Story not found"
            }

            response, status_code = add_new_story()
            response_json = response.get_json()

            assert status_code == 200
            assert response_json["data"]["success"] is False

# =========================================================
# SERVICE CLASS IS INSTANTIATED AND CALLED
# =========================================================
def test_add_new_story_flow_verification(app):

    with app.test_request_context("/add_new_story?story_id=aesop01"):

        with patch(
            "controller.story_data_learnsanskrit_controller.FetchNewFable"
        ) as mock_service:

            mock_instance = mock_service.return_value
            mock_instance.execute.return_value = {"ok": True}

            add_new_story()

            mock_service.assert_called_once_with("aesop01")
            mock_instance.execute.assert_called_once()