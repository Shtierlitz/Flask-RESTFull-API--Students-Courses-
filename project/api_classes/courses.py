from flask import abort
from flask_restful import Resource, reqparse
from project.models import *
from sqlalchemy import update, delete
from project.secondary_functions.scripts import query_courses

Session = db.session


class QueryCourses(Resource):

    def get(self):
        """Returns the list of all courses
       ---
       tags:
        - Courses
       summary:
         Courses list
       description:
         Returns the list of all courses
       operationId:
         get_courses_list
       responses:
         200:
           description: OK
         404:
           description: Not found
         505:
           description: Internal server error

       """
        with Session() as session:
            courses = session.query(Course).order_by(Course.id).all()
            if not courses:
                return abort(404)
            return query_courses(courses), 200

    def post(self):
        """Adding new course to the data base
           ---
              tags:
              - Courses
              parameters:
              - name: course_name
                in: formData
                schema:
                  type: string
                required: true
                description: Name of the course to add to the base.
              - name: description
                in: formData
                schema:
                  type: string
                required: true
                description: Description of the course.
              responses:
                200:
                 description: OK
                404:
                 description: Not found
                505:
                 description: Internal server error
           """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='course_name', required=True, type=str,
                            location='form')
        parser.add_argument(name='description', required=True, type=str,
                            location='form')
        args = parser.parse_args()

        with Session() as session:
            course = Course(name=args['course_name'], description=args['description'])
            session.add(course)
            session.commit()
            return f"Successfully added course {args['course_name']}", 200


class QueryCourse(Resource):
    def get(self, course_id):
        """Returns course by it's ID
          ---
              tags:
                - Courses
              parameters:
                - name: course_id
                  in: path
                  schema:
                    type: integer
                  required: true
                  description: Numeric ID of the course to get.
              responses:
                200:
                  description: OK
                404:
                  description: Not found
                505:
                  description: Internal server error
          """
        with Session() as session:
            query = session.query(Course).filter(Course.id == course_id).all()
            if not query:
                return abort(404)
            return query_courses(query), 200

    def put(self, course_id):
        """Updates a course info by it's ID
                ---
              tags:
              - Courses
              parameters:
                - name: course_id
                  in: path
                  schema:
                    type: integer
                  required: true
                  description: ID of the Course that need to be updated.
                - name: course_name
                  in: formData
                  schema:
                    type: string
                  required: true
                  description: Name of the course that need to be updated.
                - name: description
                  in: formData
                  schema:
                    type: string
                  required: true
                  description: New description of the course.
              responses:
                200:
                  description: OK
                404:
                  description: Not found
                505:
                  description: Internal server error
                                           """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='course_name', required=True, type=str,
                            location='form')
        parser.add_argument(name='description', required=True, type=str,
                            location='form')
        args = parser.parse_args()
        with Session() as session:
            session.execute(
                update(Course).where(Course.id == course_id).values(name=args['course_name'],
                                                                    description=args['description']))
            session.commit()

        return f"put_success. pk:{course_id} new name = {args['course_name']}, description ={args['description']}", 200

    def delete(self, course_id):
        """Deletes a course by it's ID
               ---
              tags:
              - Courses
              parameters:
                - name: course_id
                  in: path
                  schema:
                    type: integer
                  required: true
                  description: ID of the course that need to be deleted.
              responses:
                200:
                  description: OK
                404:
                  description: Not found
                505:
                  description: Internal server error
                                                   """
        with Session() as session:
            session.execute(delete(Course).filter(Course.id == course_id))
            session.commit()
            return f"successfully deleted course id:{course_id}"
