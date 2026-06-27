from flask import jsonify, request
from services.sanskrit_samskrutam_metadata_extraction_pipeline.get_metadata import GetMetaData
from services.sanskrit_samskrutam_metadata_services import retrieve_all
from services.sanskrit_samskrutam_fable_extraction_pipeline.extract_new_fable_sanskrit_samskrutam import ExtractNewFable



def write_meta_data():
    try:
        req = GetMetaData()
        res = req.execute()
        
        if res:    
            return jsonify({
                "success": True,
                "message": "Metadata extracted and written successfully.",
                "data": res
            }), 200
            
        return jsonify({
            "success": False,
            "message": "Pipeline executed but no data was processed."
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500
        
        
def retrieve_all_unused():
    response = retrieve_all()
    
    if response :
        return jsonify(response),200
    
    return jsonify(response),500


def add_new_story():
    try:
        story_id = request.args.get("story_id")

        if not story_id:
            return jsonify({
                "success": False,
                "message": "story_id query parameter is required."
            }), 400

        req = ExtractNewFable(story_id)
        res = req.execute()

        if res.get("success"):
            return jsonify(res), 200

        return jsonify(res), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500



    