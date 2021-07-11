from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os
from keras.models import load_model
import os
from keras.preprocessing import image
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from keras.applications.vgg16 import preprocess_input, decode_predictions

import tensorflow as tf

import base64
from io import BytesIO
from PIL import Image


classifier = load_model('equipment_detector.h5')

stored_dict = {'[0]': 'bench', '[1]': 'dumbbell', '[2]': 'leg-extension', '[3]': 'leg-press'}
stored_dict_n = {'[0]': 'bench', '[1]': 'dumbbell', '[2]': 'leg-extension', '[3]': 'leg-press'}
#gpu_devices = tf.config.experimental.list_physical_devices('GPU')
#for device in gpu_devices:
   #tf.config.experimental.set_memory_growth(device, True)
config =  tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
app = Flask(__name__)

#API that returns image with detections on it
@app.route('/image', methods= ['POST'])
def get_image():
    
    image_data = request.json["image"]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im.save('image22.jpg')

    image_path = 'image22.jpg'
    img = image.load_img(image_path, target_size=(256,256))
    img = image.img_to_array(img)
    img = img/255 #convert to grayscale
    img = np.expand_dims(img, axis=0)

    result = classifier.predict(img, 1, verbose=0)

    class_predicted = np.argmax(result, axis=1)

    os.remove(im)
    try:
        return Response(response=class_predicted, status=200, mimetype='image/png')
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)