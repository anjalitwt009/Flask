from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import cv2 as cv
# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model_resnet.h5'
#MODEL_PATH = 'models/model.h5' #for the already trained model 

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          
print('Model loaded. Start serving...')

#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        mask_image=mask_img(img_path,preds)
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            
        pred_class = decode_predictions(preds, top=1)  
        result = str(pred_class[0][0][1])               
        return result
    return None

def mask_img(img_path,preds):
    if preds==lungs:
        im_color = cv.imread(img_path, cv.IMREAD_COLOR)
        im_gray = cv.cvtColor(im_color, cv.COLOR_BGR2GRAY)
        _, mask = cv.threshold(im_gray, thresh=180, maxval=255, type=cv.THRESH_BINARY)
        im_thresh_gray = cv.bitwise_and(im_gray, mask)

        mask3 = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)  # 3 channel mask
        mask3 = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)  # 3 channel mask

        cv.imshow("original image", im_color)
        cv.imshow("binary mask", mask)
        cv.imshow("3 channel mask", mask3)
        cv.imshow("im_thresh_gray", im_thresh_gray)
        cv.imshow("im_thresh_color", im_thresh_color)
        cv.waitKey(5000)

if __name__ == '__main__':
    app.run(debug=True)

