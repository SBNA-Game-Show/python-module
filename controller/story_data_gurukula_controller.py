from flask import jsonify, request

from services.gurukula.meta_data.extract_meta_data import ExtractGuruKulaMetaData
from services.gurukula_metadata_services import retrieve_all

def write_meta_data():
    try:
        req = ExtractGuruKulaMetaData()
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
    if response:
        return jsonify(response),200
    
    return jsonify(response),500
    
        