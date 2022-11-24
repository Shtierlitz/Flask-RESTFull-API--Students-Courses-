from flask import abort
from flask_restful import Resource, reqparse
from project.models import *
from sqlalchemy import update, delete
from project.secondary_functions.scripts import query_students

Session = db.session


class QueryStudents(Resource):
    """Student class"""

    def get(self):
        """Returns the list of all students
       ---
       tags:
        - Students
       summary:
         Student list
       description:
         Returns the list of all students
       operationId:
         get_student_list
       responses:
         200:
           description: OK
         404:
           description: Not found
         505:
           description: Internal server error

       """
        with Session() as session:
            students = session.query(Student).order_by(Student.id).all()
            if not students:
                return abort(404)
            return query_students(students), 200

    def post(self):
        """Adding student to the data base
   ---
      tags:
      - Students
      parameters:
      - name: first_name
        in: formData
        schema:
          type: string
        required: true
        description: First name of the student to add to the base.
      - name: last_name
        in: formData
        schema:
          type: string
        required: true
        description: Second name of the student to add to the base.
      responses:
        200:
         description: OK
        404:
         description: Not found
        505:
         description: Internal server error
   """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='first_name', required=True, type=str,
                            location='form')
        parser.add_argument(name='last_name', required=True, type=str,
                            location='form')
        args = parser.parse_args()

        with Session() as session:
            student = Student(first_name=args['first_name'], last_name=args['last_name'])
            session.add(student)
            session.commit()
            return f"Successfully added student {args['first_name']} {args['last_name']}", 200


class QueryStudent(Resource):

    def get(self, student_id):
        """Returns student by it's ID
  ---
      tags:
        - Students
      parameters:
        - name: student_id
          in: path
          schema:
            type: integer
          required: true
          description: Numeric ID of the student to get.
      responses:
        200:
          description: OK
        404:
          description: Not found
        505:
          description: Internal server error
  """
        with Session() as session:
            query = session.query(Student).filter(Student.id == student_id).all()
            if not query:
                return abort(404)
            return query_students(query), 200

    def put(self, student_id):
        """Updates a student info by it's ID
        ---
      tags:
      - Students
      parameters:
        - name: student_id
          in: path
          schema:
            type: integer
          required: true
          description: ID of the student that need to be updated.
        - name: first_name
          in: formData
          schema:
            type: string
          required: true
          description: First name of the student that need to be updated.
        - name: last_name
          in: formData
          schema:
            type: string
          required: true
          description: Second name of the student that need to be updated.
      responses:
        200:
          description: OK
        404:
          description: Not found
        505:
          description: Internal server error
                                   """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='first_name', required=True, type=str,
                            location='form')
        parser.add_argument(name='last_name', required=True, type=str,
                            location='form')
        args = parser.parse_args()
        with Session() as session:
            session.execute(
                update(Student).where(Student.id == student_id).values(first_name=args['first_name'],
                                                                       last_name=args['last_name']))
            session.commit()

        return f"successfully updated student pk:{student_id} first_name: {args['first_name']}, last_name: {args['last_name']}", 200

    def delete(self, student_id):
        """Deletes a student by it's ID
       ---
      tags:
      - Students
      parameters:
        - name: student_id
          in: path
          schema:
            type: integer
          required: true
          description: ID of the student that need to be deleted.
      responses:
        200:
          description: OK
        404:
          description: Not found
        505:
          description: Internal server error
                                           """
        with Session() as session:
            session.execute(delete(Student).filter(Student.id == student_id))
            session.commit()
            return f"successfully deleted course id:{student_id}"


class QueryStudentsCourses(Resource):
    def post(self, student_id, course_id):
        """Adding student to a course by ID and course.id
           ---
        tags:
        - Students
        parameters:
          - name: student_id
            in: path
            schema:
              type: integer
            required: true
            description: ID of the student to be added to the course.
          - name: course_id
            in: path
            schema:
              type: integer
            required: true
            description: ID of the course in which the student must be added.
        responses:
          200:
            description: OK
          404:
            description: Not found
          505:
            description: Internal server error
           """
        with Session() as session:
            stud = session.query(Student).filter(Student.id == student_id).first()
            cours = session.query(Course).filter(Course.id == course_id).first()
            stud.course_rel.append(cours)
            session.commit()
            return f"Successfully added student {stud.first_name} {stud.last_name} to the course: {cours.name}"

    def delete(self, student_id, course_id):
        """Removing a student from a course by student ID and course ID
       ---
       tags:
         - Students
       parameters:
         - name: student_id
           in: path
           type: integer
           required: true
           description: ID of the student to be removed from the course..
         - name: course_id
           in: path
           type: integer
           required: true
           description: ID of the course from which the student is to be removed.

       responses:
         200:
           description: OK
         404:
           description: Not found
         505:
           description: Internal server error
       produces:
         - application/json
       """
        with Session() as session:
            stud = session.query(Student).filter(Student.id == student_id).first()
            cours = session.query(Course).filter(Course.id == course_id).first()
            stud.course_rel.remove(cours)
            session.commit()
            return f"Student {stud.first_name} {stud.last_name} id: {student_id} successfully removed from course: {cours.name}"


class QueryStudentCourse(Resource):
    def get(self, course_name):
        """Finding all students related to the course with a given name.
      ---
    tags:
      - Students
    parameters:
      - name: course_name
        in: path
        schema:
          type: string
        required: true
        description: Course name.
    responses:
      200:
        description: OK
      404:
        description: Not found
      505:
        description: Internal server error

      """
        with Session() as session:
            student = session.query(Student).select_from(Course).join(Course.stud_rel).filter(
                Course.name == course_name).all()
            if not student:
                return abort(404)
            return query_students(student), 200
