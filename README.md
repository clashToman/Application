# API Documentation for FastAPI Project

## Overview
This project is a FastAPI-based application for managing orders, products, and users for a business that sells dairy and flowers. The API supports two roles: `admin` and `user`, and provides functionality for order placement, product management, authentication using OTP, and location-based features.


### Notes:
- Order statuses include `pending`, `shipped`, and `delivered`. Delivered orders are automatically moved to order history.
- Location is fetched using the IP API at `https://ipapi.co/json/`.
- Authentication uses OTP-based login without passwords.
- User actions are restricted based on their assigned category access.

## Run the Project

# Make a clone 

* To create a environment to run the project

```bash
python3 -m venv env
```
 -m is stands for "module".
 venv is the built-in python module used to create virtual environment.
 env is that name of the "venv" folder name, can we use any name for this folder

```bash
env/activate/scrptis
```
* After the activation need to install requirement file.

```bash
pip install -r requirements.txt
```
* To check the installed package list

```bash
pip list
```
* To run the code:
```bash
uvicorn main:app --reload
```

* After the run and check the process use the command for deactivate.

 ```bash
deactivate
```

Access the API documentation at `http://localhost:8000/docs`.

