import logging

import azure.functions as func
import cv2
import urllib.request
import numpy as np
import io

def Flip(img, dir): # Vertically = 0, Horizontally = 1
    if not(dir==0 or dir==1):
        return False
    return cv2.flip(img, dir)

def Rotate(img, degree):
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def ConvertToGrayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def Resize(img, percent): # percent = 1~1000
    if(percent <= 0 or percent > 1000):
        return False
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def GenerateThumbnail(img):
    dim = (1280, 720)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def RotateRight(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

def RotateLeft(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

def processor(img_url, s):
    ops = []
    s = s.split(' ')
    url_response = urllib.request.urlopen(img_url)
    img = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

    for i in s:
        i = i.strip().split(',')
        ops.append(i)

    for op in ops:
        if(op[0].lower() == 'flip'):
            img = Flip(img, int(op[1]))
        if(op[0].lower() == 'rotate'):
            img = Rotate(img, int(op[1]))
        if(op[0].lower() == 'grayscale'):
            img = ConvertToGrayscale(img)
        if(op[0].lower() == 'resize'):
            img = Resize(img, int(op[1]))
        if(op[0].lower() == 'thumbnail'):
            img = GenerateThumbnail(img)
        if(op[0].lower() == 'rotatel'):
            img = RotateLeft(img)
        if(op[0].lower() == 'rotater'):
            img = RotateRight(img)

    return img

def numpy_to_binary(arr):
    is_success, buffer = cv2.imencode(".jpg", arr)
    io_buf = io.BytesIO(buffer)
    print(type(io_buf))
    return io_buf.read()
 

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    img = req.params.get('img')
    ops = req.params.get('ops')
    mimetype = "image/" + img[img.rfind('.')+1:]

    try:
        if img and ops:
            img = processor(img, ops)
            binary_img = numpy_to_binary(img)
            return func.HttpResponse(binary_img, mimetype = mimetype)
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass img and ops in the query string or in the request body for a personalized response.",
                status_code=200
            )
    except:
        return func.HttpResponse("Please check the parameters. The image url must contain the file type. The flip method only accepts 0 and 1. The resize method only accepts 1 to 1000")
