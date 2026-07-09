import os
from pathlib import Path
from flask import jsonify, request
from werkzeug.utils import secure_filename
from services.file_upload_services.json_reader import ReadUploadedJSON

BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data")
)

print(BASE_PATH)


def process_uploaded_file():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    # sanitize filename first
    filename = secure_filename(file.filename)

    # extract extension safely
    extension = Path(filename).suffix.lower()
    mime_type = file.content_type

    file_category = _determine_file_category(extension)

    os.makedirs(BASE_PATH, exist_ok=True)

    file_path = os.path.join(BASE_PATH, filename)
    file.save(file_path)

    service_result = _determine_service_execution(file_category, filename)

    return jsonify({
        "success": True,
        "filename": filename,
        "category": file_category,
        "mime_type": mime_type,
        "result": service_result
    }), 200


def _determine_service_execution(file_category, filename):
    """
    Route services using ONLY filename.
    """

    if file_category == "pdf":
        return "PDF processed successfully"

    if file_category == "image":
        return "Image processed successfully"

    if file_category == "document":
        return "Text document processed successfully"

    if file_category == "json":
        service = ReadUploadedJSON(filename)
        result = service.execute()
        
        return result

    return "UNKNOWN FILE TYPE"


def _determine_file_category(extension):
    pdf_extensions = {".pdf"}
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    document_extensions = {".txt", ".rtf", ".doc", ".docx"}
    json_extensions = {".json"}

    if extension in pdf_extensions:
        return "pdf"

    if extension in image_extensions:
        return "image"

    if extension in document_extensions:
        return "document"

    if extension in json_extensions:
        return "json"

    return "unknown"