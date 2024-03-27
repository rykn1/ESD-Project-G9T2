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





