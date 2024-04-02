# SMU ESD-Project-G9T2
## Jing Hang, Keith, Khidir, Ren Yi, Wesley, Ziming

# TravelBuddy

## Introduction
A 1 stop solution for all travellers. Travel with ease and like the breeze.

## Features
- Plan your Itineraries with AI, save itineraries to your account or send it to your email
- Buy flexible travel products, payment via stripe & receipt emailed to you
- Translate effortlessly by uploading image file (For this simple service, kindly use the Sample Image located in the SampleImageTranslator), use it for the translation microservice
- Login Account to store your information such as saved itineraries

# Prerequisites
- This Application is built for WINDOWS, NOT configured for MACS
- Before you begin, ensure you have done up the following pre-requirements:

## Download from google drive all additional files
### Link: 
- https://drive.google.com/drive/folders/1G1TBeM3uf6U4IRtG9B3iTb6MjZvb7ndI?usp=sharing
- Files : tessdata Folder, Arial_Unicode_MS.TTF

## Download ESD-PROJECT-G9T2 Zipfile from Github / Uploaded Zipfile / ELEARN 
- Place it under 'www' in WAMP folder, login page url should appear like this filepath: http://localhost/ESD-PROJECT-G9T2/LoginService/login.html

## !!! Run following SQL code in phpmyadmin
- PlannerComplex -> users.sql
- Shopping Complex -> cart.sql
- Shopping Complex -> shopping.sql

## API Keys Required
To ensure the program runs, insert your own API keys that can be made for free. 

### PlannerComplex
- **generative_ai.py gemeniai**: 
- **currency_service.py exchangerateio**: 
- **weather.py openweather**: 

### ShoppingComplex
- **payment.py stripe public key**: 
- **payment.py stripe secret key**: 

### TranslationComplex
- **translation.py**: 
- **translation.py (alternative key)**:  

### LoginService
- **login.js firebase keys**: 
    const firebaseConfig = {
        apiKey: "",
        authDomain: "",
        projectId: "",
        storageBucket: "",
        messagingSenderId: "",
        appId: ""
    };

# How to run 
## Steps to run TravelBuddy:
- 1. Download this repository & place it in WAMP, www folder
- 2. Place tessdata Folder and Arial_Unicode_MS.TTF in TranslationComplex folder 
- 3. Run WAMP
- 4. In compose.yaml, change the username to your docker username
- 5. docker compose up 
- 6. Set the viewport to IPhone 14 Pro Max
- 7. Run this URL -> http://localhost/ESD-PROJECT-G9T2/LoginService/login.html
- 8. Sign up for an account, use an email that you can open to receive receipts. Afterwards, it will auto re-directs you to home page to access our services

### NOTE FOR SHOP - YOU WILL BE REDIRECTED TO STRIPE API
- Email: Use an email that you can receive emails in as the receipt will be sent to you there
- For Stripe Payment: 
- Card Information: 4242 4242 4242 4242
- MM/YY: 1/25
- CVC: 242

------------------------------------------------------------------------

# Service Explanations

## Login Service
### 1. Firebase Service
- Microservice that uses Firebase to perform authentication

## Planner Complex Microservice
### 1. planner.py 
- Orchestrates the microservices in the Planner Complex Microservice
### 2. generative_ai.py
- Microservice that performs API call to Gemini AI to retrieve AI generated itinerary as well as currency symbol for selected country in UI
### 3. currency_service.py
- Microservice awaits response and retrieves currency symbol from generative_ai and performs api call to get exchange rate against the Singapore dollar 
### 4. weather.py
- Microservice that performs API call to get climate of selected chosen in UI. 

## Shopping Complex Microservice
### 1. shopItems.py
- Extracting all of the items from the database
### 2. shoppingcart.py
- Displaying the selected items selected by the user
### 3. payment_handler.py
- Orchestrates the payment.py microservice 
- Publish a message to the rabbimq queue for notification.py 
### 4. payment.py
- Invokes the STRIPE API where user will facilitate a payment process 
### 5. notification.py
- Upon consuming the message in rabbitmq queue, it sends an email to the user 

## Translation Complex Microservice
### 1. orchestrator.py 
- Orchestrates the microservices within the Translation Complex Microservice.
### 2. detect.py
- Detects words in images using pytesseract OCR.
### 4. translation.py
- Retrieves extracted words and translates them using the Deep Translator API.
### 3. text_replacement.py
- Overlays the existing image with translated text using the Python Imaging Library (PIL).
### 5. error.py
- Displays error messages.

## BTL - Kong API - Grafana & Prometheus
- For microservice status tracking 

