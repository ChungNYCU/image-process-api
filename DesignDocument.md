# Design Document

This repository contains the documentation for [Image process](https://github.com/ChungNYCU/image-process-api) API.

#### Contents

- [Considerations](#1-considerations)
    - [Assumptions](#11-assumptions)
    - [Constraints](#12-constraints)
- [Architecture](#2-architecture)
    - [Overview](#21-overview)
    - [System Context Diagrams](#22-system-context-diagrams)
    - [Component Diagrams](#23-component-diagrams)
    - [Deployment Diagrams](#24-deployment-diagrams)
- [Client Design Sample](#3-client-design-sample)
    - [Client Sample 1](#31-client-sample-1)
    - [Client Sample 2](#32-client-sample-2)
- [Appendices and References](#4-appendices-and-references)
    - [Definitions and Abbreviations](#41-definitions-and-abbreviations)
    - [References](#42-references)


## 1. Assumptions and Constraints


#### 1.1 Assumptions

##### 1.1.1 Design patterns
For this RPC API, I decided to use the Chain of Responsibility design pattern from Behavioral Design Patterns because I must deal with multiple operations from users on the image. Chain of Responsibility can let me pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. So that I can make sure each image process request is nicely made.

I have considered using Template Method. Template Method is a behavioral design pattern that defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure. Because users may upload various image formats, using the Template Method can handle different image formats situations very well, but then I decided to normalize the images received by the API and then perform image processing. There is not necessary to make templates for different image formats.

##### 1.1.2 Single Responsibility Principle
When I first designed this RPC API, SRP made me think about the meaning of Single Responsibility. Is every operation on an image a Responsibility? Or is the operation on an image itself a Responsibility?

The answer I came to was that the operation of the image itself is a kind of Responsibility. Assuming that every operation type on the image is a kind of Responsibility, I will design seven APIs to achieve seven different operations. Then, when the user wants to perform multiple operations on the same image, he needs to call the API separately and then repeatedly send the same image to the server—knowing that the image upload time is much longer than the server processing time. So, I decided to design an API and let the user specify their operations and send it with an image so that I only need to spend the time to upload the image once. Another solution is to temporarily store the image on the server and then use the unique ID to access the image. The seven APIs can also save the time of uploading the image, but I don't want to save the user's image, so I did not use this solution in the end.

##### 1.1.3 Image URL or upload image
I use an image URL instead of uploading an image because I don't want to keep the user's image, so I want users to choose a cloud storage service they trust and provide the image URL to use the image process API.

##### 1.1.4 GET or POST
There are three reasons I choose GET, not POST. The first reason is that POST needs to send JSON body, including many data such as images through multipart requests, but my API only accepts an image URL and seven different types of operation, not so complex. The second reason is I do not provide services for uploading pictures; in other words, I do not need to create or update any data in the database. The last reason is that it is more efficient and easy to use GET because you can save a GET request as a bookmark, cache it, or use it in the URL bar.


#### 1.2 Constraints

##### 1.2.1 Image URL
Image URL need to be publicly accessible.

##### 1.2.2 Image format
Only allow users to upload the jpg, jpeg, png, bmp, tiff, and tif image format because my service uses the OpenCV package.

##### 1.2.3 Image size
The image size recommended under 7,680 x 4,320 pixels.

##### 1.2.4 Number of operations
Unlimited, but URL length must be less than 2048 characters.


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


## 2. Architecture


#### 2.1 Overview
This is an RPC API capable of simple manipulation of images. Using the Chain of Responsibility design pattern from Behavioral Design Patterns.


#### 2.2 System Context Diagrams
![](https://i.imgur.com/AX2lijY.png)


#### 2.3 Component Diagrams
![](https://i.imgur.com/lssP2RM.png)


#### 2.4 Sequence diagrams
![](https://i.imgur.com/B8kF7oY.png)


#### 2.5 Deployment Diagrams
![](https://i.imgur.com/8keANcG.png)
Source: [Microsoft](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/serverless/web-app)


## 3 Client Design Sample


#### 3.1 Client Sample 1

##### 3.1.1 User Interface:
![](https://i.imgur.com/rtb4pQa.png)

##### 3.1.2 Code:
```html
<!DOCTYPE html>
<html>
<body>

<h2>Image processor</h2>

<form action="https://image-process.azurewebsites.net/api/processimage">
  <label for="img">Image URL:</label><br>
  <input type="text" id="img" name="img" size="50" value="https://i.imgur.com/IMUhhEQ.jpg"><br>
  <label for="ops">Process operations:</label><br>
  <input type="text" id="ops" name="ops" size="50" value="Flip,0"><br><br>
  <input type="submit" value="Submit">
</form> 

<p>Process operations sample: Flip,0 Resize,50 Grayscale Rotate,45</p>
<p>If you click the "Submit" button, the form-data will be sent to a page called "https://image-process.azurewebsites.net/api/processimage".</p>

</body>
</html>
```

##### 3.1.3 Demonstration:
![](https://i.imgur.com/k7Rl8H4.gif)


#### 3.2 Client Sample 2

##### 3.2.1 User Interface:
![](https://i.imgur.com/LInsE5L.png)

##### 3.2.2 Code:
```html
<!DOCTYPE html>
<html>
<body>

<h2>Image processor</h2>

<form action="https://image-process.azurewebsites.net/api/processimage">
    <label for="img">Image URL:</label><br>
    <input type="text" id="img" name="img" size="50" value="https://i.imgur.com/IMUhhEQ.jpg"><br>

    Flip:   <input type="text" name="flip" id="flip"><br>
    Rotate: <input type="text" name="rotate" id="rotate"><br>
    Resize: <input type="text" name="resize" id="resize"><br>
    Convert to grayscale: <input type="checkbox" id="grayscale" name="grayscale"><br>
    Generate a thumbnail: <input type="checkbox" id="thumbnail" name="thumbnail"><br>
    Rotate left: <input type="checkbox" id="rotatel" name="rotatel"><br>
    Rotate right:   <input type="checkbox" id="rotater" name="rotater"><br>
     
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
        var q = ''
        if(flip){
            q += 'flip,' + flip + ' '
        }
        if(rotate){
            q += 'rotate,' + rotate + ' '
        }
        if(resize){
            q += 'resize,' + resize + ' '
        }
        if(grayscale==true){
            q += 'grayscale, '
        }
        if(thumbnail==true){
            q += 'thumbnail, '
        }
        if(rotatel==true){
            q += 'rotatel, '
        }
        if(rotater==true){
            q += 'rotater, '
        }
        document.getElementById('ops').value = q;
    }

</script>

<p>Flip only accept 0 = vertically or 1 = horizontally, resize only accept 1~1000</p>
<p>If you click the "Submit" button, the form-data will be sent to a page called "https://image-process.azurewebsites.net/api/processimage".</p>

</body>
</html>
```

##### 3.2.3 Demonstration:
![](https://i.imgur.com/lHUm4Vs.gif)


## 4 Appendices and References


#### 4.1 Definitions and Abbreviations
1. URL: Uniform resource locator
2. URI: Uniform resource identifier
3. API: Application programming interface

#### 4.2 References
1. Bradski, G. (2000). The OpenCV Library. Dr. Dobb&#x27;s Journal of Software Tools.