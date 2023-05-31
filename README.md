# "Students-Courses" Flask RESTful API

## Description
Flask application implementing RESTful api technology.   
Learning project for inserting/selecting/updating/deleting courses and students who study them.

## Technologies used
`Python`, `Flask`, `Flask rest framework`, `SQLAlchemy`, `Flask-CLI`, `PostgreSQL`, `Flasgger/Swagger_ui`, `pytest`

## Getting started

To make it easy for you to get started with Django Weather Reminder, 
here's a list of recommended next steps.

## Download
Download the repository with this command: 
```bash
git clone https://github.com/Shtierlitz/Flask-RESTful-API--Students-Courses-.git
```
## Create Files
For the local server to work correctly, create your own file `local_settings.py` 
and place it in a folder next to the file `settings.py` of this Flask project.
You will also need to create `.env` file and place it in the root of the project.

### Required contents of the local_settings.py file:
```python  
# project/local_settings.py
import os

from flask_swagger_ui import get_swaggerui_blueprint

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath("courses_app.py"))
DB_HOST = os.environ.get('DATABASE_HOST')
DB_USER = os.environ.get('DATABASE_USER')
DB_NAME = os.environ.get('DATABASE_NAME')
DB_PASS = os.environ.get('DATABASE_PASSWORD')
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": 'Shtierlitzs-Python-Flask-RESTFull-API'}
    )
```

### Required contents of the .env file:
```python
SECRET_KEY='<your SECRET key>'  
DATABASE_NAME="<database name>"  
DATABASE_USER="<database username>"  
DATABASE_PASS="<database password>"  
DATABASE_HOST='localhost'
```

# Localhost development (only)

## Flask run
### Preparations
Before using the app you must ensure that you have installed PostgreSQL server in your local machine, and   
you have created database.  
You need to create data that generates by db_fil.py
Use command:
```bash
flask fill_db
```

### Venv
You need to create a virtual environment and install all dependencies  

To create virtual environment go to the root directory and run:
```bash
python -m venv venv
```

Run virtual environment:
```bash
venv/scripts/activate
```

After you can install dependencies:
```bash
pip install -r requirements.txt
```

### Run app
To run localhost server just get to the `project/` folder and then run the command:
```bash
flask run
```

## Test 
To run tests from the localhost you need to return into root directory and run:  
```bash
pytest tests\test.py
````
## Api 
### You can follow the following paths to use the `API`:
After running `flask run` you can choose two links to use swagger:  
http://localhost:5000/swagger/  
or   
http://localhost:5000/apidocs/

You should be able to see next swagger on the screen:
![Swagger](../docs_images/swagger_1.png)
![Swagger](../docs_images/swagger_2.png)


# Sources

SQLalchemy https://www.sqlalchemy.org/

Design API https://pages.apigee.com/rs/apigee/images/api-design-ebook-2012-03.pdf

OpenAPI and Swagger Editor https://www.youtube.com/watch?v=hPzorok-gI4&t=167s

