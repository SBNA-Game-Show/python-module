from flask import Blueprint
from flasgger import swag_from


from controller.story_data_sanskrit_samskrutam_controller import write_meta_data


san_samskrutam_meta_bp = Blueprint("san_samskrutam_meta_bp",__name__)


meta_data_controller = swag_from("../swaggerdocs/sanskrit_samskrutam_meta/add_metadata.yml")(write_meta_data)
san_samskrutam_meta_bp.route("/writeMetaData",methods=["POST"])(meta_data_controller)