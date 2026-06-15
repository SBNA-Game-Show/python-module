
from flask import jsonify,request
from services.learnsanskrit_metadata_services import RetrieveAllStoryDataLearnSanskrit
from services.learnsanskrit_fable_extraction_pipeline.extract_new_fable_learnsanskrit import FetchNewFable
from services.learnsanskrit_metadata_extraction_pipeline.write_to_DB import WriteLearnSanskritCCMetaData


def write_meta_data():
    req = WriteLearnSanskritCCMetaData()
    response = req.execute()
    
    return jsonify(response),200
    
def fetch_all_story_data():

    service = RetrieveAllStoryDataLearnSanskrit()

    response = service.retrieve_all()

    if response["success"]:
        return jsonify(response), 200

    return jsonify(response), 500

## Adding a new story to the collection
def add_new_story():

    # FETCH QUERY PARAM
    story_id = request.args.get("story_id")

    # validate input
    if not story_id:
        return jsonify({
            "success": False,
            "message": "story_id query parameter is required"
        }), 400

    service = FetchNewFable(story_id)
    result = service.execute()

    return jsonify({
        "data": result
    }), 200



