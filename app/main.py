from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Environment Constants
KONG_ADMIN_CDN_UPLOAD_URL = os.environ.get('KONG_ADMIN_CDN_UPLOAD_URL', 'http://kong:8000/cdn/upload')
KONG_ADMIN_CDN_RETRIEVE_URL = os.environ.get('KONG_ADMIN_CDN_RETRIEVE_URL', 'http://kong:8000/cdn/retrieve')

def validate_upload():
    if 'file' not in request.files:
        return False, "No file part"
    if request.files['file'].filename == '':
        return False, "No selected file"
    return True, ""

@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"message": "Route not found"}), 404

@app.route('/')
def index():
    return 'App is running'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        is_valid, error_message = validate_upload()
        
        if not is_valid:
            return jsonify({"message": error_message}), 400

        file = request.files['file']

        response = requests.post(
            KONG_ADMIN_CDN_UPLOAD_URL,
            files={'file': (file.filename, file.stream)}
        )

        if response.status_code != 201:
            return jsonify({"message": "Upload failed"}), 500
            
        return jsonify({"url": response.text}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve/<fileName>', methods=['GET'])
def retrieve(fileName):
    try:
        response = requests.get(
            f'{KONG_ADMIN_CDN_RETRIEVE_URL}/{fileName}',
        )

        if response.status_code == 404:
            return response.json(), 404
        if response.status_code != 200:
            return jsonify({"message": "Retrieval failed"}), 500

        return jsonify({"url": response.text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
