from flask import Flask, request, jsonify, send_from_directory
import os
import datetime

app = Flask(__name__)

KONG_ADMIN_URL = os.environ.get('KONG_ADMIN_URL', 'http://localhost:8000')

@app.before_request
def before_request():
    if os.path.exists('assets') and os.path.isdir('assets'):
        print('Asset folder exists')
    else:
        os.makedirs('assets')

@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"message": "Route not found"}), 404

def generate_unique_id():
    current_time = datetime.datetime.now()
    unique_id = current_time.strftime('%Y%m%d%H%M%S%f')
    return unique_id

def generate_unique_url(fileName):
    uniqueId = generate_unique_id();
    uniqueFileName = uniqueId + '-' + fileName;
    return KONG_ADMIN_URL + '/cdn/assets/' + uniqueFileName;

@app.route('/')
def index():
    return 'CDN is running';

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file'];
        fileName = file.filename
        file.save(os.path.join('assets/', fileName))
        return generate_unique_url(fileName), 201;
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve/<fileName>', methods=['GET'])
def retrieve(fileName):
    try:
        assets_folder = os.path.join(app.root_path, 'assets')
    
        if os.path.exists(assets_folder + '/' + fileName):
            return generate_unique_url(fileName), 200;
        else:
            return jsonify({"message": "File doesn't exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assets/<fileName>')
def serve_asset(fileName):
    try:
        if fileName == '' or '-' not in fileName:
            return jsonify({"message": "Invalid file"}), 500

        splittedFileName = fileName.split('-')
        fileName = splittedFileName[-1]

        assets_folder = os.path.join(app.root_path, 'assets')
    
        if os.path.exists(assets_folder + '/' + fileName):
            return send_from_directory(assets_folder, fileName)
        else:
            return jsonify({"message": "File doesn't exist"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)