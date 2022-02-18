# Design Document

This repository contains the documentation for [Image process]() API.

#### Contents

- [Considerations](#1-considerations)
    - [Assumptions](#11-assumptions)
        - [Design patterns](#111-design-patterns)
        - [Single Responsibility Principle](#112-single-responsibility-principle)
    - [Constraints(WIP)](#12-constraints)
- [Architecture](#2-architecture)
  - [WIP](#)

## 1. Considerations


#### 1.1 Assumptions

##### 1.1.1 Design patterns
For this RESTful API, I decided to use the Chain of Responsibility design pattern from Behavioral Design Patterns because I must deal with multiple operations from users on the image. Chain of Responsibility can let me pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. So that I can make sure each image process request is nicely made.

I have considered using Template Method. Template Method is a behavioral design pattern that defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure. Because users may upload various image formats, using the Template Method can handle different image formats situations very well, but then I decided to normalize the images received by the API and then perform image processing. There is not necessary to make templates for different image formats.

##### 1.1.2 Single Responsibility Principle
When I first designed this RESTful API, SRP made me think about the meaning of Single Responsibility. Is every operation on an image a Responsibility? Or is the operation on an image itself a Responsibility?

The answer I came to was that the operation of the image itself is a kind of Responsibility. Assuming that every operation type on the image is a kind of Responsibility, I will design seven APIs to achieve seven different operations. Then, when the user wants to perform multiple operations on the same image, he needs to call the API separately and then repeatedly send the same image to the server—knowing that the image upload time is much longer than the server processing time. So, I decided to design an API and let the user specify their operations and send it with an image so that I only need to spend the time to upload the image once. Another solution is to temporarily store the image on the server and then use the unique ID to access the image. The seven APIs can also save the time of uploading the image, but I don't want to save the user's image, so I did not use this solution in the end.

#### 1.2 Constraints
*In this section describe any constraints on the system that have a significant impact on the design of the system.*

#### 1.3 System Environment
*In this section describe the system environment on which the software will be executing. Include any specific reasons why this system was chosen and if there are any plans to include new sections to the list of current ones.*

## 2. Architecture


#### 2.1 Overview
*Provide here a descriptive overview of the software/system/application architecture.*

#### 2.2 Component Diagrams
*Provide here the diagram and a detailed description of its most valuable parts. There may be multiple diagrams. Include a description for each diagram. Subsections can be used to list components and their descriptions.*

#### 2.3 Class Diagrams
*Provide here any class diagrams needed to illustrate the application. These can be ordered by which component they construct or contribute to. If there is any ambiguity in the diagram or if any piece needs more description provide it here as well in a subsection.*

#### 2.4 Sequence Diagrams
*Provide here any sequence diagrams. If possible list the use case they contribute to or solve. Provide descriptions if possible.*

#### 2.5 Deployment Diagrams
*Provide here the deployment diagram for the system including any information needed to describe it. Also, include any information needed to describe future scaling of the system.*

#### 2.6 Other Diagrams
*Provide here any additional diagrams and their descriptions in subsections.*

## 3 User Interface Design
*Provide here any user interface mock-ups or templates. Include explanations to describe the screen flow or progression.*

## 4 Appendices and References


#### 4.1 Definitions and Abbreviations
*List here any definitions or abbreviations that could be used to help a new team member understand any jargon that is frequently referenced in the design document.*

#### 4.2 References
*List here any references that can be used to give extra information on a topic found in the design document. These references can be referred to using superscript in the rest of the document.*