# Project Structure

Provides documentation on how this project is setup, detailing purposes of files and folders.


## Folders

### ***docker***
Docker related items
- Dockerfile - Instructions to create a docker container for the receipts API. 
- docker-compose.yml - Defines networks, volumues and services required for the receipts api to work

### **logs**
Directory to store application logs

### **src**
Contains application source files

- `main.py`: Application start point
- `helpers.py` contains global helper functions

    ### **repo**:
    Contains global data repo for CRUD

    #### **database**:
    Contains databsae setup and connection handlers
    - `db.py`: contains sqlalchemy engine, db session generator, and database setup function

    #### **exceptions**:
    Contains exception handlers and errors
    - `exceptions_handlers.py`: All exception handlers
    - `exceptions.py`: Possible exceptions that can be thrown

    #### **receipts**:
    Contains everything related to the receipts service/endpoint
    - `controller.py`: Endpoints for the receipts service
    - `model.py`: contains the database models
    - `schema.py`: contains data models
    - `service.py`: contains functions to pull data from the database
    - `receipt_repo`: receipt data repo that inherits global repo
    - `points_repo`: receipt data repo that inherits global repo
    - `exceptions.py`: exception specific to the receiepts repo

    #### **utils**
    Contains utility functions for the application
    - `config.py`: contains application settings
    - `logger.py`: contains setup logger configuration


### **tests**
Contains unit tests

### **conf**
Contains logging config

### **examples**
Contains sample data








