import os
import traceback
from flask import Blueprint, jsonify, current_app, request,send_file
from src.domains.processor import start
from src.domains.zip import ZipManager

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/analyze', methods=['POST'])
async def upload_file():
    # check if file exists in request
    if 'file' not in request.files:
        return jsonify({"filename": None, "analysis": None, "error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"filename": None, "analysis": None, "error": "No file selected"}), 400
    # save fuploaded file to directory and process pdf
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        output_folder = current_app.config['OUTPUT_FOLDER']

        zipper = ZipManager(output_base=output_folder)
        pdf_name = file.filename.split('.')[0]
        pdf_path = os.path.join(upload_folder, file.filename)
        file.save(pdf_path)  # Save uploaded file to uploads/
        print(f"[upload router]Started Processing PDF {file.filename}")
        checklistpath = await start(pdf_path, output_folder)
        # process_pdf_all(pdf_path, output_folder, dpi=400)
        download_filename = file.filename.split('.')[0] + '_checklist.txt'
        return zipper.create_zip_from_folder(pdf_name)
        # return send_file(checklistpath,as_attachment=True,download_name=download_filename,mimetype="application/octet-stream")
        #  return jsonify({
        #     "filename": file.filename,
        #     "analysis": f"PDF processed successfully! Outputs are in '{output_folder}/'.",
        #     "error": None
        # })
    except Exception as e:
        print(f'Something went wrong {str(e)}')
        print(traceback.format_exc())
        return jsonify({
            "filename": None,
            "analysis": None,
            "error": str(e)
        }), 500
