# flask_web/app.py

from flask import Flask, request, Response, json, url_for, send_from_directory
from werkzeug import secure_filename
import os
import uuid
import glob
import subprocess
from functools import wraps
from PIL import Image
import pytesseract

UPLOAD_PATH = './uploads'
STATIC_PATH = './static'
STATIC_URL_PATH = '/public'
FILE_EXT = '.jpeg'

application = Flask(__name__, static_url_path=STATIC_URL_PATH)

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


def url_join(*args):
    return '/'.join(arg.strip('/') for arg in args)

@application.route("/")
def hello():
    return 'Here is where the magic happens.'

@application.route('/uploads', methods=['POST'])
def create_upload():

    upload_id = uuid.uuid4().hex
    folder_path = upload_folder_path(upload_id)
    os.makedirs(folder_path)

    link = url_for('upload', upload_id=upload_id, _external=True)

    data = {'upload_id': upload_id, 'link': link}

    resp = response_json(data, 201)

    resp.headers['Link'] = link

    return resp


@application.route('/uploads', methods=['GET'])
def get_uploads():

    folders = [os.path.basename(f) for f in glob.glob(
        os.path.join(UPLOAD_PATH, '**'))]

    data = [{'upload_id': f, 'link': url_for(
        'upload', upload_id=f, _external=True)} for f in folders]

    return response_json(data)


@application.route('/uploads/<string:upload_id>', methods=['POST'])
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


@application.route('/uploads/<string:upload_id>', methods=['GET'])
@upload_exists
def get_upload(upload_id):

    folder_path = upload_folder_path(upload_id)

    return '', 200


@application.route('/uploads/<string:upload_id>/stitch', methods=['POST'])
@upload_exists
def stitch(upload_id):

    folder_path = upload_folder_path(upload_id)
    path_pattern = os.path.join(folder_path, '*')
    files = os.listdir(folder_path)

    if(len(files) < 2):
        return response_error('To peform a stitch, you must upload 2 images at least.')

    file_ext = os.path.splitext(files[0])[1]

    static_folder_path = os.path.join(STATIC_PATH, upload_id)

    if(os.path.exists(static_folder_path) == False):
        os.mkdir(static_folder_path)

    file_result_path = os.path.join(static_folder_path, f'result{file_ext}')

    public_path = url_join(request.host_url, STATIC_URL_PATH, upload_id, f'result{file_ext}')

    cmd = f'stitcher Default {file_result_path} {path_pattern}'

    print(f'Executing command: {cmd}')

    try:

        subprocess.check_call([cmd], shell=True)
        print(f'Public path is {public_path}')
        return response_json({'location': public_path}, 201)

    except subprocess.CalledProcessError:

        return response_error('There was an error - command exited with non-zero code', 500)

@application.route('/uploads/<string:upload_id>/text', methods=['POST'])
def text(upload_id):

    static_folder_path = os.path.join(STATIC_PATH, upload_id)
    file_result_path = os.path.join(static_folder_path, f'result{FILE_EXT}')

    text = pytesseract.image_to_string(Image.open(file_result_path),"por")

    return text

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
