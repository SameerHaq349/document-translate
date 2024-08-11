from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from drive_service import upload_file_to_drive, download_file_from_drive
from slides_service import process_presentation
from translate_service import list_languages
import ssl
import certifi

ssl._create_default_https_context = ssl.create_default_context

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    languageCode = request.form.get('languageCode', '')
    languageName = request.form.get('language', '')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Upload and process the file
            file_id = upload_file_to_drive(file_path)
            process_presentation(file_id, languageCode, languageName)
            final_file, filename = download_file_from_drive(file_id)

            if final_file:
                return jsonify({"link": final_file})
            else:
                return jsonify({'error': 'Failed to upload file to Google Drive'}), 500
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500

@app.route("/languages", methods=['GET'])
def get_languages():
    try:
        languages = list_languages()
        return jsonify(languages)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch languages'}), 500

if __name__ == '__main__':
    app.run(debug=True)
