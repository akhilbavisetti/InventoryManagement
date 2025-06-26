# Fertiliser Retail Management System

A web application for managing fertiliser retail operations including sales, purchases, inventory management, customer and supplier management.

## Technology Stack
- Frontend: HTML, CSS
- Backend: Python Flask
- Database: MySQL

## Features
- Authentication (Login/Logout)
- Sales Management
- Purchase Management
- Inventory Management
- Customer Management
- Supplier Management
- Reporting

## Setup Instructions
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up MySQL database using the provided schema
5. Configure the database connection in `config.py`
6. Run the application: `python run.py`
7. Access the application at http://localhost:5000

## Database Design
The database is designed following normalization principles (1NF, 2NF, 3NF) with tables for users, products, customers, suppliers, sales, and purchases. 