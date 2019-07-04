# flask_web/app.py

from flask import Flask, request, Response, json, url_for
from werkzeug import secure_filename
import os
import uuid
import glob
import subprocess

app = Flask(__name__)
UPLOAD_PATH='./uploads'

print('Starting server...')

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/uploads', methods=['POST'])
def create_upload():

    upload_id = uuid.uuid4().hex
    os.makedirs(os.path.join(UPLOAD_PATH, upload_id))

    data = {
        'upload_id': upload_id
    }

    js = json.dumps(data)

    resp = Response(js, status=201, mimetype='application/json')
    resp.headers['Link'] = url_for(
        'upload', upload_id=upload_id, _external=True)

    return resp


@app.route('/uploads', methods=['GET'])
def get_uploads():

    folders = [os.path.basename(f) for f in glob.glob(os.path.join(UPLOAD_PATH, '**'))]

    return Response(json.dumps(folders), status=200, mimetype='application/json')


@app.route('/uploads/<string:upload_id>', methods=['POST'])
def upload(upload_id):

    folder_path = os.path.join(UPLOAD_PATH, upload_id)
    if(os.path.exists(folder_path) == False):
        return 'Upload doesn\'t exists', 400

    uploaded_files = request.files.getlist('file[]')

    for file in uploaded_files:
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)

    return '', 201

@app.route('/uploads/<string:upload_id>/stitch', methods=['POST'])
def stitch(upload_id):

    folder_path = os.path.join(UPLOAD_PATH, upload_id)
    if(os.path.exists(folder_path) == False):
        return 'Upload doesn\'t exists', 400

    path_pattern = os.path.join(folder_path, '*')

    cmd = f'stitcher Default target-receipt.jpeg {path_pattern}'

    print(cmd)

    subprocess.run([cmd], shell=True)

    return '', 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
