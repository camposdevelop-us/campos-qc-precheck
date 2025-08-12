import os
from flask import Blueprint, jsonify, current_app, request
from src.domains.pdf import start


upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
async def upload_file():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    output_folder = current_app.config['OUTPUT_FOLDER']
    # check if file exists in request
    if 'file' not in request.files:
        return jsonify({"filename": None, "analysis": None, "error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"filename": None, "analysis": None, "error": "No file selected"}), 400
    # save fuploaded file to directory and process pdf
    try:
        pdf_path = os.path.join(upload_folder, file.filename)
        file.save(pdf_path)  # Save uploaded file to uploads/
        print(f"[upload router]Started Processing PDF {file.filename}")
        await start(pdf_path, output_folder)
        # process_pdf_all(pdf_path, output_folder, dpi=400)

        return jsonify({
            "filename": file.filename,
            "analysis": f"PDF processed successfully! Outputs are in '{output_folder}/'.",
            "error": None
        })
    except Exception as e:
        print(f'Something went wrong {str(e)}')
        return jsonify({
            "filename": None,
            "analysis": None,
            "error": str(e)
        }), 500
