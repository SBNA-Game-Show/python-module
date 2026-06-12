from flask import Blueprint
from flasgger import swag_from


from controller.story_data_learnsanskrit_controller import fetch_all_story_data,write_meta_data,add_new_story



story_data_bp = Blueprint("story_data_bp",__name__)


story_data_bp.route("/writeMeta",methods=["POST"])(write_meta_data)

decorated_controller = swag_from("../swaggerdocs/learnsanskrit_metadata/get_available_story_data_learnsanskrit.yml")(fetch_all_story_data)
story_data_bp.route("/getAll", methods=["GET"])(decorated_controller)

#Post route that will take an id retrieve data from learn sanskrit.cc tokenize it and store it in data folder
add_new_story_controller = swag_from("../swaggerdocs/learnsanskrit_metadata/add_new_story_learnsanskrit.yml")(add_new_story)
story_data_bp.route("/addNew",methods=["POST"])(add_new_story_controller)