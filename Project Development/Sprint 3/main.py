from flask import Flask
from flask import request
from flask import make_response

import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
staticLoad = False #Useful during development
formatError = "Incorrect format"

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model('ECG.h5')
app = Flask(__name__)

def getOptAndType(name):
    type = name[name.find('.') + 1:]
    if type == "css" or type == "html":
        opt = 'r'
    else:
        opt = 'rb'
        
    return (opt, type)

staticAssets = {}
assetsDir = 'assets'
for file in os.listdir(assetsDir):
    opt, type = getOptAndType(file)
    staticAssets[file] = open(assetsDir + '/' + file, opt).read()

def createNoResourceResponse():
    res = make_response()
    res.status = "Resource not found"
    res.status_code = 404
    return res

@app.route('/')
def index():
    if staticLoad:
        indexPage = staticAssets['index.html']
    else:
        indexPage = open(assetsDir + '/' + 'index.html').read()
    return indexPage

@app.route('/about')
def about():
    return serveFile("about.html")

@app.route('/info')
def info():
    return serveFile("info.html")

@app.route('/<name>')
def serveFile(name):
    if staticLoad and name not in staticAssets.keys():
        return createNoResourceResponse()
    if not staticLoad and name not in os.listdir(assetsDir):
        return createNoResourceResponse()
    
    opt, type = getOptAndType(name)
    if staticLoad:
        file = staticAssets[name]
    else:
        file = open(assetsDir + '/' + name, opt).read()
    res = make_response(file)
    ext = {'html': 'text/html', 'css': 'text/css', 'js': 'text/javascript', 'jpg': 'image/jpg', 'png': 'image/png', 'ico': 'image/ico'}
    res.content_type = ext[type]
    
    return res

@app.post('/image')
def predictImage():
    imgFile = request.get_data(cache = False)
    try:
        img = tf.io.decode_image(imgFile)
    except:
        return formatError
    imgRGB = img
    if len(imgRGB.shape) != 3 or (imgRGB.shape[2] != 1 and imgRGB.shape[2] != 3):
        return formatError
    
    if imgRGB.shape[2] == 1:
        imgRGB = tf.image.grayscale_to_rgb(img)
        
    x = tf.image.resize(imgRGB, [64,64]).numpy()
    x = np.expand_dims(x,axis=0)
    y = np.argmax(model.predict(x),axis=1)
    index = ['Left Bundle Branch Block', 'Normal', 'Premature Atrial Contraction', 'Premature Ventricular Contractions', 'Right Bundle Branch Block','Ventricular Fibrillation']
    return index[y[0]]


if __name__ == "__main__":
    app.run(debug = False)