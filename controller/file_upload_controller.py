import os
from pathlib import Path
from flask import jsonify, request
from werkzeug.utils import secure_filename

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

    extension = Path(file.filename).suffix.lower()
    mime_type = file.content_type
    file_category = determine_file_category(extension)

    # Create data directory if needed
    os.makedirs(BASE_PATH, exist_ok=True)

    # Sanitize filename
    filename = secure_filename(file.filename)

    # Full path
    file_path = os.path.join(BASE_PATH, filename)

    # Save uploaded file
    file.save(file_path)

    return jsonify({
        "success": True,
        "filename": filename,
        "saved_path": file_path,
        "extension": extension,
        "mime_type": mime_type,
        "category": file_category
    }), 200


def determine_file_category(extension):
    pdf_extensions = {".pdf"}
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    document_extensions = {".doc", ".docx", ".txt", ".rtf"}
    spreadsheet_extensions = {".xls", ".xlsx", ".csv"}
    presentation_extensions = {".ppt", ".pptx"}

    if extension in pdf_extensions:
        return "pdf"

    if extension in image_extensions:
        return "image"

    if extension in document_extensions:
        return "document"

    if extension in spreadsheet_extensions:
        return "spreadsheet"

    if extension in presentation_extensions:
        return "presentation"

    return "unknown"