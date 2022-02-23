import azure.functions as func
import logging
from processImage import processor

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    img = req.params.get('img').strip()
    ops = req.params.get('ops').strip()
    
    if img==None or ops==None:
        return func.HttpResponse("Image url and operation are required.", status_code=400)

    try:
        img_ext = img[img.rfind('.')+1:]
        if(img_ext == 'tif'):
            img_ext = 'tiff'
            mimetype = "image/" + img_ext
        else:
            mimetype = "image/" + img_ext
    except:
        return func.HttpResponse("Image url invalid.", status_code=400)

    try:
        img = processor.img_processor(img, ops)
    except Exception as e:
        return func.HttpResponse("Image url invalid. " + str(e), status_code=400)

    try:
        binary_img = processor.numpy_to_binary('.' + img_ext, img)
    except:
        return func.HttpResponse(img, status_code=400)

    return func.HttpResponse(binary_img, mimetype = mimetype, status_code=200)