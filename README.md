# SMU ESD-Project-G9T2
## Jing Hang, Keith, Khidir, Ren Yi, Wesley, Ziming

# TravelBuddy

## Introduction
A 1 stop solution for all travellers. Travel with ease and like the breeze.

## Features
- Plan your Itineraries with AI
- Buy flexible travel products
- Translate effortlessly 

# Prerequisites
Before you begin, ensure you have met the following requirements:
- Required software (e.g. Docker).
    - Pytesseract OCR
        - FULL VIDEO GUIDE: https://www.youtube.com/watch?v=Rb93uLXiTwA&ab_channel=AllroundZone 

        ## Step-by-Step Guide
        - Install Tesseract OCR:
            - For Windows users, download Tesseract installer from [here](https://github.com/UB-Mannheim/tesseract/wiki).
            - Follow the installation steps until you reach 'Select components to install'. Make sure to select all options, including 'Additional language data (download)'.
            - Keep the Destination Folder as default and proceed with the installation.

        - Configure Environment Variables:
            - After installation, search for 'environment variables' and click on it.
            - In the Environment Variables window, select 'Path' and click Edit.
            - Click New and paste 'C:\Program Files\Tesseract-OCR' (assuming you chose the default installation path). Then click OK.


## API Keys Required
To ensure the program runs, kindly add on the following API keys to it's destinations

### PlannerComplex
- **generative_ai.py**: AIzaSyAZGQei2hEWa3YBQtHuO6TBuYK6Si6ZFC4
- **currency_service.py**: b03e781c96bd6d8f723f9845a764a569
- **weather.py**: 87b8df22e7c24f9de25392d2d0c519b7

### ShoppingComplex
- **filename.py**: API KEY

### TranslationComplex
- **translation.py**: 342731d95amsh83e40184d15719ep11f5ffjsna8e3ab0bffc3
- **translation.py (alternative key)**: 6f0e682c93msh5bcf8629d32f86bp1a79dbjsn822131d7d32d 


# How to run 
## Steps to run TravelBuddy:
- 1. KYS

------------------------------------------------------------------------

# Service Explanations & Guide

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
- 
### 2. shoppingcart.py
- Displaying the selected items selected by the user
- 
### 3. payment_handler.py
- Orchestrates the payment.py microservice 
- Publish a message to the rabbimq queue for notification.py 
### 4. payment.py
-Invokes the STRIPE API where user will facilitate a payment process 

### 5. notification.py
- Upon consuming the message in rabbitmq queue, it sends an email to the user 





