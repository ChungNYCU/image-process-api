# Image process API documentation

This repository contains the documentation for [Image process](https://github.com/ChungNYCU/image-process-api) API.

#### Contents

- [Overview](#1-overview)
- [Resources](#2-resources)
  - [Process image](#21-process-image)

## 1. Overview

This Image process API deployed on Azure can provide several functions for processing images, including Flip, Rotate, Conver to grayscale, Resize, Generate a thumbnail, Rotate left, and Rotate right, which accepts four image formats: bmp, jpeg, png, and tiff. All requests are made to endpoints beginning:

`https://image-process.azurewebsites.net/api/`

All requests must be secure, i.e. `https`, not `http`.


## 2. Resources

The API is RPC API. All requests must be made using `https`.

### 2.1. Process image

#### Sending an image with operations utilize `multipart/form-data`

```
POST https://image-process.azurewebsites.net/api/processimage
```

Example POST request header and body:
```
POST /api/processimage HTTP/1.1
User-Agent: PostmanRuntime/7.29.0
Accept: */*
Cache-Control: no-cache
Postman-Token: bc0afcb0-782d-4339-af37-9e0be5cc75de
Host: image-process.azurewebsites.net
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
 
----------------------------postman
Content-Disposition: form-data; name="img"
<[PROXY]>
----------------------------postman
Content-Disposition: form-data; name="ops"
grayscale+rotate,135+flip,1+resize,50
----------------------------postman--
```

With the following fields:

| Parameter       | Type         | Required?  | Description                                                    |
| -------------   |--------------|------------|----------------------------------------------------------------|
| Operations      | string       | required   | Specify which operation or operations to perform on the image. |

Operations:
Users can utilize the operations below to manipulate their images.  
Use ‘,’ (comma) between operation and parameter.  
Use ’ ’ (space) between each operation.  
The user can specify which operation or operations to perform on the image.  
Operations can be applied in an order specified by the caller.

| Operation name  | Parameter?   | Type       | Description                                          |
| -------------   |--------------|------------|------------------------------------------------------|
| Flip            | Required     | Int        | Flip the image, 0 for vertical, 1 for horizontal.    |
| Rotate          | Required     | Int        | Rotate the image in degrees.                         |
| Grayscale       | Not required | None       | Converts the image to grayscale.                     |
| Resize          | Required     | Int        | Resize image by percentage.                          |
| Thumbnail       | Not required | None       | Generates a thumbnail of the image.                  |
| RotateL         | Not required | None       | Rotate the image 90 degrees to the left.             |
| RotateR         | Not required | None       | Rotates the image 90 degrees to the right.           |

Example operations string:

```
grayscale rotate,135 flip,1 resize,50
```

Expected result:

![](https://i.imgur.com/qy88frp.jpg)


Accepted image formats:

* `image/bmp`
* `image/jpeg`
* `image/jpg`
* `image/png`
* `image/tiff`
* `image/tif`


Example response:
```
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: image/png
Server: Kestrel
Request-Context: appId=cid-v1:702721ea-5239-4038-8386-a584b5e1805a
Date: Fri, 25 Feb 2022 08:08:39 GMT
 
The console does not support viewing response bodies with media files.
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
| 400        | User error. Request is incorrect or corrupt, and the server can't understand it.                   |
| 405        | Wrong http method, use HTTP POST.                                                                  |
