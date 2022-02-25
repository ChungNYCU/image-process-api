import azure.functions as func
import logging
from processImage import processor


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method != 'POST':
        return func.HttpResponse("Use Http Post", status_code=405)

    try:
        ops = req.form.get('ops').strip()
    except Exception as e:
        return func.HttpResponse('Process operations failed, exception= [%s]' % e, status_code=400)

    try:
        uploadFile = req.files.get('img')
        filename = uploadFile.filename
        img = uploadFile.read()
    except Exception as e:
        return func.HttpResponse('Process file failed, exception= [%s]' % e, status_code=400)

    if img == None or ops == None:
        return func.HttpResponse("Image and operation are required.", status_code=400)

    try:
        img_ext = filename[filename.rfind('.')+1:]
        if(img_ext == 'tif'):
            img_ext = 'tiff'
            mimetype = "image/" + img_ext
        else:
            mimetype = "image/" + img_ext
    except:
        return func.HttpResponse("File extension invalid.", status_code=400)

    try:
        img = processor.img_processor(img, ops)
    except Exception as e:
        return func.HttpResponse("Image url invalid. " + str(e), status_code=400)

    try:
        binary_img = processor.numpy_to_binary('.' + img_ext, img)
    except Exception as e:
        return func.HttpResponse("Cannot convert numpy array to image. " + str(e), status_code=400)

    return func.HttpResponse(binary_img, mimetype=mimetype, status_code=200)
