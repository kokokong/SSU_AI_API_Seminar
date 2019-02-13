from __future__ import print_function
import os
from flask import Flask, render_template, redirect, url_for, request, Markup, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder = "uploads")

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '1234'

@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=["GET",'POST'])
def upload_file():
    print(request.method)

    file = request.files['image']
    if file.filename == "":
        flash("NO Selected file!!")
        return  redirect(request.url)
    filename = secure_filename(file.filename)
    ftype = filename [-4:]
    filename = "tmp"+ftype
    f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key="1234"
    app.run(debug = True)