# flask_web/app.py

from flask import Flask, request, Response, json, url_for
from werkzeug import secure_filename
import os
import uuid
import glob
import subprocess
from functools import wraps

app = Flask(__name__)
UPLOAD_PATH = './uploads'

print('Starting server...')


def response_json(data, status=200):
    return Response(json.dumps(data), status, mimetype='application/json')


def response_error(message, status=400):
    return response_json({'message': message}, status)

def upload_folder_path(upload_id):
    return os.path.join(UPLOAD_PATH, upload_id)

def upload_exists(fn):
    @wraps(fn)
    def decorator_function(*args, **kwargs):

        upload_id = kwargs['upload_id']
        folder_path = upload_folder_path(upload_id)

        if(os.path.exists(folder_path) == False):
            return response_error(f'There\'s no upload with id ${upload_id}')

        return fn(*args, **kwargs)
    return decorator_function


@app.route("/")
def hello():
    return "Stitcher API"


@app.route('/uploads', methods=['POST'])
def create_upload():

    upload_id = uuid.uuid4().hex
    os.makedirs(upload_folder_path(upload_id))

    data = {'upload_id': upload_id}

    resp = response_json(data, 201)

    resp.headers['Link'] = url_for(
        'upload', upload_id=upload_id, _external=True)

    return resp


@app.route('/uploads', methods=['GET'])
def get_uploads():

    folders = [os.path.basename(f) for f in glob.glob(
        os.path.join(UPLOAD_PATH, '**'))]

    data = [{'upload_id': f, 'link': url_for(
        'upload', upload_id=f, _external=True)} for f in folders]

    return response_json(data)


@app.route('/uploads/<string:upload_id>', methods=['POST'])
@upload_exists
def upload(upload_id):

    folder_path = upload_folder_path(upload_id)

    uploaded_files = request.files.getlist('file[]')

    if(len(uploaded_files) == 0):
        return response_json({'message': 'No file found'})

    for file in uploaded_files:
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)

    return '', 201


@app.route('/uploads/<string:upload_id>/stitch', methods=['POST'])
@upload_exists
def stitch(upload_id):

    folder_path = os.path.join(UPLOAD_PATH, upload_id)

    path_pattern = os.path.join(folder_path, '*')

    cmd = f'stitcher Default target-receipt.jpeg {path_pattern}'

    print(cmd)

    try:
        subprocess.check_call([cmd], shell=True)
        return '', 200
    except subprocess.CalledProcessError:
        return response_error('There was an error - command exited with non-zero code', 500)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
