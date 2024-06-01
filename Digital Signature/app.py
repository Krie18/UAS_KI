from flask import Flask, render_template, request, redirect, url_for
from digital_signature import DigitalSignature
import os

app = Flask(__name__)
ds = DigitalSignature()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys', methods=['GET'])
def generate_keys():
    result = ds.generate_keys()
    return result

@app.route('/sign_file', methods=['GET', 'POST'])
def sign_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            result = ds.sign_file(file_path)
            return result
    return render_template('sign_file.html')

@app.route('/verify_signature', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            result = ds.verify_signature(file_path)
            return result
    return render_template('verify_signature.html')

if __name__ == '__main__':
    app.run(debug=True)