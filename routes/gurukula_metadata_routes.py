from flask import Blueprint
from flasgger import swag_from

from controller.story_data_gurukula_controller import write_meta_data, retrieve_all_unused


gurukula_meta_bp = Blueprint("gurukula_meta_bp",__name__)

# gurukula_meta_write_controller = swag_from("../swaggerdocs/gurukula_metadata/add_metadata.yml")(write_meta_data)
# gurukula_meta_bp.route("/writegurukulaMeta",methods=["POST"])(gurukula_meta_write_controller)


# gurukula_meta_get_all_controller = swag_from("../swaggerdocs/gurukula_metadata/get_unused_stories.yml")(retrieve_all_unused)
# gurukula_meta_bp.route("/get-Unused",methods=["GET"])(gurukula_meta_get_all_controller)

gurukula_meta_bp.route("/writegurukulaMeta",methods=["POST"])(write_meta_data)


gurukula_meta_bp.route("/get-Unused",methods=["GET"])(retrieve_all_unused)