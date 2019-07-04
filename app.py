# flask_web/app.py

from flask import Flask, request
from werkzeug import secure_filename
import os
import uuid

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
    if(request.method == 'POST'):

        try:
            file = request.files['file']
        except:
            return 'No file uploaded'

        folder_path = os.path.join('./upload', upload_id)
        
        return os.mkfifo(folder_path)

        # file.save(os.path.join(folder_path, secure_filename(file.filename)))
        
    return 'Nothing to save.'

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')


