# E:\FoxMineded\Fox_september\task_10_sql\project\app.py
from flasgger import Swagger
from flask import Flask

from project.db_fil import fill_db
from project.courses_api import *
from project.models import db


def create_app(config='development'):
    app = Flask(__name__)
    if config == 'development':
        app.config.from_pyfile("local_settings.py")
    elif config == 'testing':
        app.config.from_pyfile('testing_settings.py')

    db.init_app(app)
    api.init_app(app)
    app.cli.add_command(fill_db)

    swagger = Swagger(app, template=template)

    app.register_blueprint(app.config['SWAGGER_BLUEPRINT'], url_prefix=app.config['SWAGGER_URL'])
    app.register_blueprint(api_bp)

    with app.app_context():

        db.create_all()

        return app


if __name__ == '__main__':
    app = create_app('testing')
    app.run(debug=True)
