from flask import Blueprint
from flasgger import swag_from

from controller.file_upload_controller import process_uploaded_file


upload_file_bp = Blueprint("upload_file_bp",__name__)


upload_file_bp.route("/upload",methods=["POST"])(process_uploaded_file)

