from urllib import response

from flask import jsonify, request


from services.tokenized_data_service import RetrieveTokenizedStories,RetrieveTokenizedStoryById,RetrieveTokenizedStoryByCategory,UpdateTokenizedStory


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
    
## Edit Tokenized Story
def update_tokenized_story():
    storyId = request.args.get("story_id")

    if not storyId:
        return jsonify({
            "success": False,
            "message": "Story Id is Required"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400

    try:
        updater = UpdateTokenizedStory(storyId, data)
        result = updater.update_tokenized()

        return jsonify(result), 200 if result["success"] else 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    



