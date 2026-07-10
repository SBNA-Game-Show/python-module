from flask import jsonify, request

from services.gurukula.meta_data.extract_meta_data import ExtractGuruKulaMetaData

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
        