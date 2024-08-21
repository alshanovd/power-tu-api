# Power TU
## Run the App
Run `python3 manage.py runserver` in order to run the server locally.<br>
It uses a remote MySQL server as a database.<br>

## MySQL
Use `Postman` or `Paw` in order to use API. There are all CRUD methods implemented for the Products table.


# Power TU Backend

## Overview
Power TU is a web-based analytical tool designed to help retailers and businesses analyze large datasets for better decision-making. The backend, built with Django, provides a robust API for managing data, handling user authentication, and implementing business logic. The application is designed to be scalable, secure, and easy to deploy.

## Features
- **User Authentication and Authorization**: Secure user management using Django's built-in authentication system.
- **Data Processing and Analysis**: Handles large datasets and integrates seamlessly with the frontend.
- **RESTful API**: Provides endpoints for CRUD operations on various data models.
- **Security**: Implements secure communication protocols (SSL/TLS) and role-based access control.

## Project Structure
- **accounts/**: Handles user-related functionality such as registration, login, and profile management.
- **analysis/**: Contains core analysis functionality, including data processing and visualization logic.
- **power_tu_api/**: Main project directory containing settings, URLs, and other core configurations.
- **static/**: Directory for static files (CSS, JavaScript, images).
- **manage.py**: Django's command-line utility for administrative tasks.
- **requirements.txt**: Lists the Python dependencies needed to run the project.
- **Certificates**: SSL/TLS certificates for secure communication.

## Installation

### Prerequisites
- Python 3.12
- Django 5.0
- MySQL 8.0 (or a compatible version)
- Virtual environment tool (e.g., `venv`)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/power-tu-backend.git
   cd power-tu-backend

## Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

## Install the required dependencies:
pip install -r requirements.txt

## Configure the database:
Ensure that MySQL is installed and running.
Create a database for the project and update the DATABASES setting in power_tu_api/settings.py with your database credentials.

## Apply migrations:
python manage.py migrate

## Run the development server:
python manage.py runserver

## API Documentation
The backend provides several RESTful API endpoints for managing data:

### Authentication:
POST /login/: User login.
POST /register/: User registration.
POST /logout/: User logout.

### Products:
GET /products/: Retrieve a list of products.
POST /products/: Create a new product.
PUT /products/: Update an existing product.
DELETE /products/: Delete a product.

### Orders:
GET /order-items/: Retrieve a list of orders.
POST /order-items/: Create a new order.
PUT /order-items/: Update an existing order.
DELETE /order-items/: Delete an order.

## Configuration

### Environment Variables
Make sure the following environment variables are set:

SECRET_KEY: A secret key for Django.
DEBUG: Set to False in production.
DATABASE_URL: The URL for your MySQL database.
ALLOWED_HOSTS: List of allowed hosts for the application.

## Security Settings
Configure security-related settings such as ALLOWED_HOSTS, CSRF_COOKIE_SECURE, SECURE_SSL_REDIRECT, etc., in power_tu_api/settings.py.

## Testing

### Running Unit Tests
To run the unit tests:
python manage.py test

### API Testing
Use tools like Postman or cURL to test the API endpoints. Ensure that you include the necessary authentication headers for protected endpoints.


