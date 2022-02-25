# Design Document

This repository contains the documentation for [Image process](https://github.com/ChungNYCU/image-process-api) API.

#### Contents

- [Considerations](#1-considerations)
    - [Assumptions](#11-assumptions)
    - [Constraints](#12-constraints)
    - [System Environment](#13-system-environment)
    - [Development Environment](#14-development-environment)
- [Architecture](#2-architecture)
    - [Overview](#21-overview)
    - [System Context Diagrams](#22-system-context-diagrams)
    - [Component Diagrams](#23-component-diagrams)
    - [Sequence Diagrams](#24-sequence-diagrams)
    - [Deployment Diagrams](#25-deployment-diagrams)
    - [Little Language](#26-little-language)
- [Client Design Sample](#3-client-design-sample)
    - [Client Sample 1](#31-client-sample-1)
    - [Client Sample 2](#32-client-sample-2)
- [Appendices and References](#4-appendices-and-references)
    - [Definitions and Abbreviations](#41-definitions-and-abbreviations)
    - [References](#42-references)


## 1. Considerations


#### 1.1 Assumptions

##### 1.1.1 Design patterns
For this RPC API, I decided to use the Chain of Responsibility design pattern from Behavioral Design Patterns because I must deal with multiple operations from users on the image. Chain of Responsibility can let me pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. So that I can make sure each image process request is nicely made.

I have considered using Template Method. Template Method is a behavioral design pattern that defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure. Because users may upload various image formats, using the Template Method can handle different image formats situations very well, but then I decided to normalize the images received by the API and then perform image processing. There is not necessary to make templates for different image formats.

##### 1.1.2 Single Responsibility Principle
When I first designed this RPC API, SRP made me think about the meaning of Single Responsibility. Is a different operation on an image a different Responsibility? Or is the operation on an image itself a Responsibility?

The answer I came to was that the operation of the image itself is a kind of Responsibility. Assuming that every operation type on the image is a kind of Responsibility, I will design seven APIs to achieve seven different operations. Then, when the user wants to perform multiple operations on the same image, he needs to call the API separately and then repeatedly send the same image to the server—knowing that the image upload time is much longer than the server processing time. So, I decided to design an API and let the user specify their operations and send it with an image so that I only need to spend the time to upload the image once. Another solution is to temporarily store the image on the server and then use the unique ID to access the image. The seven APIs can also save the time of uploading the image, but I don't want to save the user's image, so I did not use this solution in the end.

##### 1.1.3 Programming Language
I decided to use Python because it has good image processing libraries such as OpenCV, Pillow, etc. For the User Interface I decided to use HTML and JavaScript.


##### 1.1.4 Thumbnail operation
My thumbnail operation can turn an image to YouTube vedio thumbnail. My thumbnail operation can turn an image into a YouTube video thumbnail, which means 1280x720 resolution.

#### 1.2 Constraints

##### 1.2.1 Image formats
Only allow users to upload the jpg, jpeg, png, bmp, tiff, and tif image format because my service uses the OpenCV package.

##### 1.2.2 Image size
The image size recommended under 7,680 x 4,320 pixels.

##### 1.2.3 Number of operations
Unlimited


#### 1.3 System Environment
Browser compatibility:

| Browser name      | Supported?   |
| ------------------|--------------|
| Chrome            | Yes          |
| Edge              | Yes          |
| Firefox           | Yes          |
| Internet Explorer | Yes          |
| Opera             | Yes          |
| Safari            | Yes          |


#### 1.4 Development Environment
You can download source code from [Image process api](https://github.com/ChungNYCU/image-process-api). And utilize `pip install` to install required package.  

Python3 version: `3.9.10`

Required package:
| Package name      | Version      |
| ------------------|--------------|
| azure-functions   | `4.x`        |
| numpy             | `1.22.2`     |
| opencv-Python     | `4.5.5.62`   |
| requests          | `2.27.1`     |
| urllib3           | `1.26.8`     |


## 2. Architecture


#### 2.1 Overview
This RPC API deployed on Azure is capable of simply manipulating image. It uses the Chain of Responsibility design pattern from Behavioral Design Patterns.


#### 2.2 System Context Diagrams
![](https://i.imgur.com/XQfK1Ef.png)


#### 2.3 Component Diagrams
![](https://i.imgur.com/EUq6lQT.png)


#### 2.4 Sequence diagrams
![](https://i.imgur.com/BQRA6pR.png)


#### 2.5 Deployment Diagrams
![](https://i.imgur.com/8keANcG.png)
Source: [Microsoft](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/serverless/web-app)

#### 2.6 Little Language
Users can utilize the operations below to manipulate their images.  
Use ',' (comma) between operation and parameter.  
Use ' ' (space) between each operation.  
The user can specify which operation or operations to perform on the image.  
Operations can be applied in an order specified by the caller.  
Upon completion of the transform the user can access to the resulting image file. 

| Operation name  | Parameter?   | Type       | Description                                          |
| -------------   |--------------|------------|------------------------------------------------------|
| Flip            | Required     | Int        | Flip the image, 0 for vertical, 1 for horizontal.    |
| Rotate          | Required     | Int        | Rotate the image in degrees.                         |
| Grayscale       | Not required | None       | Converts the image to grayscale.                     |
| Resize          | Required     | Int        | Resize image by percentage.                          |
| Thumbnail       | Not required | None       | Generates a thumbnail of the image.                  |
| RotateL         | Not required | None       | Rotate the image 90 degrees to the left.             |
| RotateR         | Not required | None       | Rotates the image 90 degrees to the right.           |


## 3 Client Design Sample


#### 3.1 Client Sample 1


##### 3.1.1 User Interface:
![](https://i.imgur.com/xjb7vsD.png)

##### 3.1.2 Code:
```html
<!DOCTYPE html>
<html>

<body>

  <h2>Image processor</h2>

  <form method="POST" enctype="multipart/form-data" action="https://image-process.azurewebsites.net/api/processimage">
    <div class="form-group">
      <label for="img">File to upload: </label>
      <input type="file" class="form-control-file" id="img" name="img">
    </div>
    <label for="ops">Process operations:</label><br>
    <input type="text" id="ops" name="ops" size="50" value="Flip,0"><br><br>
    <input type="submit" value="Submit">
  </form>

  <p>Process operations sample: Flip,0 Resize,50 Grayscale Rotate,45</p>
  <p>If you click the "Submit" button, the form-data will be sent to a page called
    "https://image-process.azurewebsites.net/api/processimage".</p>

</body>

</html>
```

##### 3.1.3 Demonstration:
![](https://i.imgur.com/wG55TnG.gif)


#### 3.2 Client Sample 2


##### 3.2.1 User Interface:
![](https://i.imgur.com/aKBzmE9.png)

##### 3.2.2 Code:
```html
<!DOCTYPE html>
<html>

<body>

    <h2>Image processor</h2>

    <form method="POST" enctype="multipart/form-data" action="https://image-process.azurewebsites.net/api/processimage">
        <div class="form-group">
            <label for="img">File to upload: </label>
            <input type="file" class="form-control-file" id="img" name="img">
        </div>

        Flip: <input type="text" name="flip" id="flip"><br>
        Rotate: <input type="text" name="rotate" id="rotate"><br>
        Resize: <input type="text" name="resize" id="resize"><br>
        Convert to grayscale: <input type="checkbox" id="grayscale" name="grayscale"><br>
        Generate a thumbnail: <input type="checkbox" id="thumbnail" name="thumbnail"><br>
        Rotate left: <input type="checkbox" id="rotatel" name="rotatel"><br>
        Rotate right: <input type="checkbox" id="rotater" name="rotater"><br>

        <button onclick="generate_query_str()">Submit</button>
        <input type="hidden" id="ops" name="ops" size="50" value="">
    </form>

    <script>
        function generate_query_str() {
            var flip = document.getElementById('flip').value;
            var rotate = document.getElementById('rotate').value;
            var resize = document.getElementById('resize').value;
            var grayscale = document.getElementById('grayscale').checked;
            var thumbnail = document.getElementById('thumbnail').checked;
            var rotatel = document.getElementById('rotatel').checked;
            var rotater = document.getElementById('rotater').checked;
            var q = ' '
            if (flip) {
                q += 'flip,' + flip + ' '
            }
            if (rotate) {
                q += 'rotate,' + rotate + ' '
            }
            if (resize) {
                q += 'resize,' + resize + ' '
            }
            if (grayscale == true) {
                q += 'grayscale, '
            }
            if (thumbnail == true) {
                q += 'thumbnail, '
            }
            if (rotatel == true) {
                q += 'rotatel, '
            }
            if (rotater == true) {
                q += 'rotater, '
            }
            document.getElementById('ops').value = q;
        }

    </script>

    <p>Flip only accept 0 = vertically or 1 = horizontally, resize only accept 1~1000</p>
    <p>If you click the "Submit" button, the form-data will be sent to a page called
        "https://image-process.azurewebsites.net/api/processimage".</p>

</body>

</html>
```

##### 3.2.3 Demonstration:
![](https://i.imgur.com/fmIBrYx.gif)


## 4 Appendices and References


#### 4.1 Definitions and Abbreviations
1. URL: Uniform resource locator
2. URI: Uniform resource identifier
3. API: Application programming interface

#### 4.2 References
1. Bradski, G. (2000). The OpenCV Library. Dr. Dobb&#x27;s Journal of Software Tools.
