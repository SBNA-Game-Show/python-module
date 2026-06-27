from flask import jsonify, request
from services.sanskrit_samskrutam_metadata_extraction_pipeline.get_metadata import GetMetaData

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