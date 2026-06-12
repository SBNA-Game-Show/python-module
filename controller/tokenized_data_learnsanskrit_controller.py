from urllib import response

from flask import jsonify, request

from services.retrieve_all_tokenized_stories import RetrieveTokenizedStories
from services.tokenized_data_service.tokenized_data_service import RetrieveTokenizedStoryById
from services.retrieve_tokenized_stories_by_category import RetrieveTokenizedStoryByCategory



    
## Get All tokenized stories from collection

def fetch_all_tokenized_stories():
    
    service = RetrieveTokenizedStories()
    response = service.get_all()
    
    if response["success"]:
        return jsonify(response),200
    
    return jsonify(response),500
    

## Get tokenized story by id

def fetch_tokenized_story_by_id():

    # FETCH QUERY PARAM
    story_id = request.args.get("story_id")

    # VALIDATE INPUT
    if not story_id:

        return jsonify({
            "success": False,
            "message": "story_id query parameter is required"
        }), 400

    # CALL SERVICE
    service = RetrieveTokenizedStoryById(story_id)

    story = service.retrieve_story()

    # SUCCESS RESPONSE
    return jsonify({
        "success": True,
        "data": story
    }), 200
    

## Get tokenized story by category

def fetch_tokenized_stories_by_category():
    category = request.args.get("category_name")
    
    if not category:
        return jsonify({
            "success":False,
            "message":"Category Name is Required"
        }),400
        
    service = RetrieveTokenizedStoryByCategory(category)
    data = service.get_by_category()
    
    return jsonify({
        "success": True,
        "data": data
    }),200
    



