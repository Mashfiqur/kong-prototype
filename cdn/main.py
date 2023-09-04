from flask import Flask, request, jsonify, send_from_directory
import os
import datetime
import uuid

app = Flask(__name__)

# Configuration
KONG_ADMIN_URL = os.environ.get('KONG_ADMIN_URL', 'http://localhost:8000')
ASSETS_FOLDER = 'assets'

# Dictionary to store file name and unique CDN URL mapping
ASSET_UNIQUE_IDS = {}

def generate_unique_id():
    current_time = datetime.datetime.now()
    return current_time.strftime('%Y%m%d%H%M%S%f') + str(uuid.uuid4())

def purify_file_name(fileName):
    return fileName.replace(" ", "_").strip().lower()

def generate_cdn_url(fileName):
    return f'{KONG_ADMIN_URL}/cdn/assets/{fileName}'

def validate_upload():
    if 'file' not in request.files:
        return False, "No file part"
    if request.files['file'].filename == '':
        return False, "No selected file"
    return True, ""

@app.before_request
def before_request():
    if not os.path.exists(ASSETS_FOLDER):
        os.makedirs(ASSETS_FOLDER)

@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"message": "Route not found"}), 404

@app.route('/')
def index():
    return 'CDN is running'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        isValid, error_message = validate_upload()
        
        if not isValid:
            return jsonify({"message": error_message}), 400

        file = request.files['file']
        fileName = purify_file_name(file.filename)
        uniqueId = generate_unique_id()

        ASSET_UNIQUE_IDS[fileName] = uniqueId

        file.save(os.path.join(ASSETS_FOLDER, fileName))

        return generate_cdn_url(uniqueId), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve/<fileName>', methods=['GET'])
def retrieve(fileName):
    try:
        fileName = purify_file_name(fileName)

        if fileName not in ASSET_UNIQUE_IDS:
            return jsonify({"message": "File doesn't exist"}), 404

        assetUniqueId = ASSET_UNIQUE_IDS[fileName]
        file_path = os.path.join(ASSETS_FOLDER, fileName)

        if os.path.exists(file_path):
            return generate_cdn_url(assetUniqueId), 200
        else:
            return jsonify({"message": "File doesn't exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assets/<uniqueID>')
def serve_asset(uniqueID):
    try:
        fileName = next((k for k, v in ASSET_UNIQUE_IDS.items() if v == uniqueID), None)
        if not fileName:
            return jsonify({"message": "File doesn't exist"}), 404

        file_path = os.path.join(ASSETS_FOLDER, fileName)

        if os.path.exists(file_path):
            return send_from_directory(ASSETS_FOLDER, fileName)
        else:
            return jsonify({"message": "File doesn't exist"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
