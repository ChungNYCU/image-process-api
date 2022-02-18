# Image process API documentation

This repository contains the documentation for [Image process]() API.

#### Contents

- [Overview](#1-overview)
- [Resources](#2-resources)
  - [Process image](#21-process-image)

## 1. Overview

The Image process API provides several functions for processing images, including Flip, Rotate, Conver to grayscale, Resize, Generate a thumbnail, Rotate left, and Rotate right, which accepts four image formats: bmp, jpeg, png, and tiff. Image process API is a JSON-based OAuth2 API. All requests are made to endpoints beginning:
`https://api.WIP.com/v1`

All requests must be secure, i.e. `https`, not `http`.


## 2. Resources

The API is RESTful and arranged around resources. All requests must be made using `https`.

### 2.1. Process image

#### Uploading an image url with operations

This requires multipart form-encoded data.

```
POST https://api.WIP.com/v1/processImage?img=&ops=
```

Example request:

```
POST /v1/images HTTP/1.1
Host: api.WIP.com
Content-Length: 428
Content-Type: multipart/form-data; boundary=abc123
Accept: application/json
Accept-Charset: utf-8

--abc123
Content-Disposition: form-data; name="Operations"
Content-Type: application/json
{
    "img": "https://i.imgur.com/diyu2YU.jpg",
    "ops": "Flip,0+Resize,50+Grayscale+Rotate,45"
}

--abc123
Content-Disposition: form-data; name="image"; filename="filename.jpeg"
Content-Type: image/jpeg

IMAGE_DATA
--abc123--
```

With the following fields:

| Parameter       | Type         | Required?  | Description                                                    |
| -------------   |--------------|------------|----------------------------------------------------------------|
| Operations       | string       | required   | Specify which operation or operations to perform on the image. |

Operations:

| Operation name  | Parameter?   | Type       | Description                                          |
| -------------   |--------------|------------|------------------------------------------------------|
| Flip            | Required     | Int        | Flip the image, 0 for vertical, 1 for horizontal.    |
| Rotate          | Required     | Int        | Rotate the image in degrees.                         |
| Grayscale       | Not required | None       | Converts the image to grayscale.                     |
| Resize          | Required     | Int        | Resize image by percentage.                          |
| Thumbnail       | Not required | None       | Generates a thumbnail of the image.                  |
| RotateL         | Not required | None       | Rotate the image 90 degrees to the left.             |
| RotateR         | Not required | None       | Rotates the image 90 degrees to the right.           |

Example operations:

```
processImage?img=url&ops=Flip,0+Resize,50+Grayscale+Rotate,45
```

Expected result:

![](https://i.imgur.com/qy88frp.jpg)


The field name must be `image`. All lines in the body must be terminated with `\r\n`. Only one image may be sent per request. The following image content types are supported:

* `image/bmp`
* `image/jpeg`
* `image/png`
* `image/tiff`


The response is a binary data stream. Example response:
```
HTTP/1.1 200 OK 
Last-Modified: Fri, 10 Feb 2012 14:31:06 GMT
Content-Type: image/jpeg
Content-Length: 20331
Server: WEBrick/1.3.1 (Ruby/1.9.2/2011-02-18)
Date: Fri, 10 Feb 2012 14:31:22 GMT
Connection: Keep-Alive
```

Binary data stream example:
```
����JFIF��C			





	


��C

```

Possible errors:

| Error code | Description                                                                                        |
| -----------|----------------------------------------------------------------------------------------------------|
| 400        | Request is incorrect or corrupt, and the server can't understand it.                               |
| 403        | User does not have read permission to the file ID.                                                 |
| 404        | File ID is not found, or in rare cases the converted image cannot be returned.                     |
| 415        | File ID is not supported image (jpeg, png, bmp or tiff).                                           |
