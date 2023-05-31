# project/courses_api.py

from flask import Blueprint
from flask_restful import Api

from project.api_classes.courses import QueryCourses, QueryCourse
from project.api_classes.groups import QueryGroups, QueryGroup
from project.api_classes.students import QueryStudents, QueryStudent, QueryStudentsCourses, QueryStudentCourse

api_bp = Blueprint('Api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

template = {
    "info": {
        "description": "Flask RestFull API project",
        "version": "'1.0.0",
        "title": "Students and Courses",
        "contact": {
            "email": "rollbar1990@gmail.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "host": "localhost",
        "basePath": "api",
        "schemes": ["http", "https"],
        "operationID": "getmycourses"
    },
    "swagger": "2.0",
    "paths": {}
}

api.add_resource(QueryGroups, '/groups')
api.add_resource(QueryGroup, '/groups/<int:group_id>')

api.add_resource(QueryCourses, '/courses')
api.add_resource(QueryCourse, '/courses/<int:course_id>')

api.add_resource(QueryStudents, '/students')
api.add_resource(QueryStudent, '/students/<int:student_id>')
api.add_resource(QueryStudentsCourses, '/courses/<int:course_id>/students/<int:student_id>')
api.add_resource(QueryStudentCourse, '/students/<course_name>/courses')
