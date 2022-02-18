# import cv2
# import urllib.request
# import numpy as np

# def Flip(img, dir): # Vertically = 0, Horizontally = 1
#     if not(dir==0 or dir==1):
#         return img
#     res = cv2.flip(img, dir)
#     return res

# def Rotate(img, degree):
#     (h, w) = img.shape[:2]
#     (cX, cY) = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
#     res = cv2.warpAffine(img, M, (w, h))
#     return res

# def ConvertToGrayscale(img):
#     res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     return res

# def Resize(img, percent): # percent = 1~1000
#     if(percent <= 0):
#         percent = 1
#     if(percent > 1000):
#         percent = 1000
#     width = int(img.shape[1] * percent / 100)
#     height = int(img.shape[0] * percent / 100)
#     dim = (width, height)
#     res = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#     return res

# def GenerateThumbnail(img):
#     dim = (1280, 720)
#     res = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#     return res

# def RotateRight(img):
#     res = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
#     return res

# def RotateLeft(img):
#     res = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
#     return res

# def processor(img_url, s):
#     ops = []
#     s = s.split('+')
#     url_response = urllib.request.urlopen(img_url)
#     img = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

#     for i in s:
#         i = i.strip().split(',')
#         ops.append(i)

#     for op in ops:
#         if(op[0] == 'Flip'):
#             img = Flip(img, int(op[1]))
#         if(op[0] == 'Rotate'):
#             img = Rotate(img, int(op[1]))
#         if(op[0] == 'Grayscale'):
#             img = ConvertToGrayscale(img)
#         if(op[0] == 'Resize'):
#             img = Resize(img, int(op[1]))
#         if(op[0] == 'Thumbnail'):
#             img = GenerateThumbnail(img)
#         if(op[0] == 'RotateL'):
#             img = RotateLeft(img)
#         if(op[0] == 'RotateR'):
#             img = RotateRight(img)
            
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

#     return img

#img_url = 'https://i.imgur.com/diyu2YU.jpg'
#s = "Flip,0+Resize,50+Grayscale+Rotate,45"