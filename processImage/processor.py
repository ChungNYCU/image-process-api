import cv2
import io
import numpy as np
import urllib.request


def flip(img, dir):  # Vertically = 0, Horizontally = 1
    return cv2.flip(img, dir)


def rotate(img, degree):
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
    return cv2.warpAffine(img, m, (w, h))


def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def resize(img, percent):  # percent = 1~1000
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def generate_thumbnail(img):
    THUMBNAIL_WIDTH = 1280
    THUMBNAIL_HEIGHT = 720
    dim = (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def rotate_right(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)


def rotate_left(img):
    return cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)


def img_processor(img, ops_str):
    ops = []
    ops_str = ops_str.lower()
    ops_str = ops_str.split(' ')

    try:
        img = cv2.imdecode(np.array(bytearray(img), dtype=np.uint8), -1)
    except Exception as e:
        return "Image decode failed:" + str(e)

    for i in ops_str:
        i = i.strip().split(',')
        ops.append(i)

    for op in ops:
        if op[0] == 'flip':
            try:
                dir = int(op[1])
            except:
                return 'The flip operation requires a integer parameter.'

            if dir == 0 or dir == 1:
                img = flip(img, dir)
            else:
                return 'The flip operation only accepts 0 or 1 as a parameter.'

        elif op[0] == 'rotate':
            try:
                degree = int(op[1])
            except:
                return 'The rotate operation requires a integer parameter.'

            img = rotate(img, degree)
        elif op[0] == 'grayscale':
            img = convert_to_grayscale(img)
        elif op[0] == 'resize':
            try:
                percentage = int(op[1])
            except:
                return 'The resize operation requires a integer parameter.'

            if percentage > 0 and percentage <= 1000:
                img = resize(img, percentage)
            else:
                return 'The resize operation only accepts 1 to 1000 as a parameter.'

        elif op[0] == 'thumbnail':
            img = generate_thumbnail(img)
        elif op[0] == 'rotatel':
            img = rotate_left(img)
        elif op[0] == 'rotater':
            img = rotate_right(img)
        elif op[0] == '':
            continue
        else:
            return op[0] + ' is invalid operation.'

    return img


def numpy_to_binary(img_ext, img_arr):
    is_success, buffer = cv2.imencode(img_ext, img_arr)
    io_buf = io.BytesIO(buffer)
    return io_buf.read()
