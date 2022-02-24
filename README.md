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

#### Sending an image url with operations

```
GET https://image-process.azurewebsites.net/api/processimage HTTP/1.1
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

Example URI:

```
https://image-process.azurewebsites.net/api/processimage?img=https://i.imgur.com/IMUhhEQ.jpg&ops=grayscale+rotate,135+flip,1+resize,50
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
Content-Type: image/jpg
Server: Kestrel
Request-Context: appId=cid-v1:702721ea-5239-4038-8386-a584b5e1805a
Date: Wed, 23 Feb 2022 04:07:52 GMT
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
