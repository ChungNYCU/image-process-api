import azure.functions as func
import cv2
import io
import logging
import numpy as np
import urllib.request


def flip(img, dir): # Vertically = 0, Horizontally = 1
    if not (dir==0 or dir==1):
        return False
    return cv2.flip(img, dir)


def rotate(img, degree):
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
    return cv2.warpAffine(img, M, (w, h))


def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def resize(img, percent): # percent = 1~1000
    if(percent <= 0 or percent > 1000):
        return False
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


def generate_thumbnail(img):
    THUMBNAIL_WIDTH = 1280
    THUMBNAIL_HEIGHT = 720
    dim = (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


def rotate_right(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)


def rotate_left(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)


def img_processor(img_url, ops_str):
    ops = []
    ops_str = ops_str.lower()
    ops_str = ops_str.split(' ')
    url_response = urllib.request.urlopen(img_url)
    img = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

    for i in ops_str:
        i = i.strip().split(',')
        ops.append(i)

    for op in ops:
        if(op[0] == 'flip'):
            img = flip(img, int(op[1]))
        if(op[0] == 'rotate'):
            img = rotate(img, int(op[1]))
        if(op[0] == 'grayscale'):
            img = convert_to_grayscale(img)
        if(op[0] == 'resize'):
            img = resize(img, int(op[1]))
        if(op[0] == 'thumbnail'):
            img = generate_thumbnail(img)
        if(op[0] == 'rotatel'):
            img = rotate_left(img)
        if(op[0] == 'rotater'):
            img = rotate_right(img)

    return img

def numpy_to_binary(img_ext, img_arr):
    is_success, buffer = cv2.imencode(img_ext, img_arr)
    io_buf = io.BytesIO(buffer)
    return io_buf.read()

def raise_exception_msg(msg, status_code=400):
    return func.HttpResponse(msg, status_code)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    img = req.params.get('img')
    ops = req.params.get('ops')
    
    if not (img and ops):
        return raise_exception_msg("image url and operation are required")

    img_ext = img[img.rfind('.')+1:]
    mimetype = "image/" + img_ext

    try:
        if img and ops:
            img = img_processor(img, ops)
            binary_img = numpy_to_binary('.' + img_ext, img)
            return func.HttpResponse(binary_img, mimetype = mimetype)
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass img and ops in the query string or in the request body for a personalized response.",
                status_code=200
            )
    except:
        return func.HttpResponse("Please check the parameters. The image url must contain the file type. The flip method only accepts 0 and 1. The resize method only accepts 1 to 1000")
