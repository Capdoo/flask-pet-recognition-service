from flask import Flask, jsonify, request
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
import numpy as np
import urllib.request

app = Flask(__name__)


@app.route('/')
def index():
    return "Una vez una tarde llevaba a un niño un pollo a la espalda y el pollo el maestro no sabía qué cosa está llevando y quería preguntarle al maestro y le decía quería hacerle caerles ya preguntarle si estaba vivo o estaba muerto si estaba muerto le enseñaba el pollo vivo pero si estaba vivo perdón si estaba muerto decir un mayor decía que estaba muerto el niño del profesor entrega el niño le entregaba vivo pero si le decía que está muy esté vivo el niño torres y el cuello del pollo y le enseñaba el cuello el pollo muerto no sabía qué hacer el niño estaba con esa trampa para hacer el maestro y le pregunta el niño al maestro louis profesor maestro dígame el pollo que tengo en las manos está vivo" 


@app.route('/imagen')
def recognizer():

    link_reference = request.json['reference']
    link_bullet = request.json['bullet']

    _nameReference = 'reference.jpg'
    _nameBullet = 'bullet.jpg'
    _nameRedim = 'redim.jpg'

    save_image(link_reference,_nameReference)
    save_image(link_bullet,_nameBullet)

    if(isReferenceBigger(_nameReference, _nameBullet)):
        #resize de referencia
        resize(_nameReference,_nameBullet,_nameRedim)
        imageA = cv2.imread(_nameBullet) #What is not touched
    else:
        #resize de bullet
        resize(_nameBullet,_nameReference,_nameRedim)
        imageA = cv2.imread(_nameReference) #What is not touched

    imageB = cv2.imread(_nameRedim)

    # Convert gray scale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    mse = mse(grayA, grayB)
    print("SSIM: {}".format(score))

    #cv2.imshow("Original", imageA)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return jsonify({"SSIM":format(score), "MSE":format(mse)})

def mse (imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def isReferenceBigger(_nameReference, _nameBullet):
    reference = cv2.imread(_nameReference)
    width_reference = reference.shape[1]
    height_reference = reference.shape[0]
    indexReference = width_reference*height_reference

    bullet = cv2.imread(_nameBullet)
    width_bullet = bullet.shape[1]
    height_bullet = bullet.shape[0]
    indexBullet = width_bullet*height_bullet

    return indexReference > indexBullet

def save_image(link,_newName):
    urllib.request.urlretrieve(link, _newName)
# I want to resize this image, 
# with the dimensions of this image, 
# and save it with this name
def resize(original_route, dimensions_route, new_name):
    #ExtractNewDimensions
    img1 = cv2.imread(dimensions_route)
    new_width = img1.shape[1]
    new_height = img1.shape[0]
    dsize = (new_width, new_height)

    #Destiny
    img2 = cv2.imread(original_route)
    output = cv2.resize(img2, dsize)
    cv2.imwrite(new_name,output)

if __name__ == '__main__':
    app.run(debug=True, port=4000)


