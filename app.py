# flask_web/app.py

from flask import Flask, request
from werkzeug import secure_filename
import os
import uuid
import glob

app = Flask(__name__)

print('Starting server...')

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/uploads', methods=['POST'])
def create_upload():
    folder = uuid.uuid4().hex
    os.makedirs('./upload/'+folder)
    return folder
    

@app.route('/uploads/<string:upload_id>', methods = ['POST'])
def upload(upload_id):

    try:
        file = request.files['file']
    except:
        return 'No file uploaded'

    folder_path = os.path.join('./upload', upload_id)

    if(os.path.exists(folder_path)==False):
        return 'Upload doens\'t exists', 400

    last_count = len(glob.glob(os.path.join(folder_path,'*'))) + 1
    file_name = f'part_{last_count}{os.path.splitext(file.filename)[1]}'
    file_path = os.path.join(folder_path, file_name)

    file.save(file_path)

    return '', 201
        
    return 'Nothing to save.'


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')


