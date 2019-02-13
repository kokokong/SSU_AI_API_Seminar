from __future__ import print_function
import os
from flask import Flask, render_template, redirect, url_for, request, Markup, flash, send_from_directory
from werkzeug.utils import secure_filename
import time
import matplotlib.pyplot as plt
import requests
import cv2
import operator
import numpy as np
from PIL import Image
from io import BytesIO

# Variables
_region = None#Here you enter the region of your subscription
_url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
_key = "Your Key" #Here you have to paste your primary key
_maxNumRetries = 10

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
    return redirect(url_for('result',file=filename))


@app.route('/result/<file>')
def result(file):
    #"""
    image_path = r'./uploads/'+file
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': _key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.

    result = response.json()
    print(result)
    image_caption = result["description"]["captions"][0]["text"].capitalize()
    message = Markup("<h1>"+image_caption+"</h1>")
    flash(message)
    print(image_path)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
    #full_filename = "/uploads/"+file
    full_filename = "/" + file
    print(full_filename)
    #return send_from_directory('uploads',file)
    return render_template('output.html',file= file)

@app.route('/uploads/<file>')
def send_file(file):
    return send_from_directory(UPLOAD_FOLDER, file)

if __name__ == '__main__':
    app.secret_key="1234"
    app.run(debug = True)