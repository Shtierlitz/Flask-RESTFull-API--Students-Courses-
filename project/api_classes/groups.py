from flask import abort
from flask_restful import Resource, reqparse
from project.models import *
from sqlalchemy import func, update, delete
from project.secondary_functions.scripts import query_groups

Session = db.session


class QueryGroups(Resource):
    def get(self):
        """Returns the list of all groups or finds all groups with less or equals student count
        ---
        tags:
         - Groups
        summary:
          Group list
        description:
          Returns the list of all groups
        operationId:
          get_group_list
        parameters:
        - name: stud_count
          in: query
          schema:
            type: integer
          required: false
          description: Specifies the number of students up to which to find them.
        responses:
          200:
            description: OK
          404:
            description: Not found
          505:
            description: Internal server error

        """
        parser = reqparse.RequestParser()
        parser.add_argument(name='stud_count', required=False, type=int, help="Number of students in group",
                            location='args')
        args = parser.parse_args()
        if args['stud_count']:
            with Session() as session:
                groups_id = session.query(Student.group_id).join(Group).group_by(Student.group_id).having(
                    func.count(Student.group_id) <= args['stud_count'])
                groups = session.query(Group).filter(Group.id.in_(groups_id)).order_by(Group.id).all()
                if not groups:
                    return abort(404)
                return query_groups(groups), 200

        with Session() as session:
            groups_list = session.query(Group).order_by(Group.id).all()
            return query_groups(groups_list), 200

    def post(self):
        """Adding group to the data base
           ---
              tags:
              - Groups
              parameters:
              - name: name
                in: formData
                schema:
                  type: string
                required: true
                description: Name of a new group.
              responses:
                200:
                 description: OK
                404:
                 description: Not found
                505:
                 description: Internal server error
           """
        parser = reqparse.RequestParser()
        parser.add_argument(name='name', required=True, type=str, help="New name of group",
                            location='form')
        args = parser.parse_args()
        if args['name']:
            with Session() as session:
                group = Group(name=args['name'])
                session.add(group)
                session.commit()
                return f"post_success. new added group = {args['name']}", 200
        return abort(404)


class QueryGroup(Resource):
    def get(self, group_id):
        """Returns group by it's ID
  ---
      tags:
        - Groups
      parameters:
        - name: group_id
          in: path
          schema:
            type: integer
          required: true
          description: Numeric ID of the group to get.
      responses:
        200:
          description: OK
        404:
          description: Not found
        505:
          description: Internal server error
  """
        with Session() as session:
            query = session.query(Group).filter(Group.id == group_id).all()
            if not query:
                return abort(404)
            return query_groups(query), 200

    def put(self, group_id):
        """Updates a group name by it's ID
        ---
      tags:
      - Groups
      parameters:
        - name: group_id
          in: path
          schema:
            type: integer
          required: true
          description: ID of the student that need to be updated.
        - name: group_name
          in: formData
          schema:
            type: integer
          required: true
          description: A new name of a group.
      responses:
        200:
          description: OK
        404:
          description: Not found
        505:
          description: Internal server error
                                   """
        parser = reqparse.RequestParser()
        parser.add_argument(name='group_name', required=True, type=str, help="New name of group",
                            location='form')
        args = parser.parse_args()
        with Session() as session:
            session.execute(update(Group).where(Group.id == group_id).values(name=args['group_name']))
            session.commit()

            return f"put_success. pk:{group_id} new name = {args['group_name']}", 200

    def delete(self, group_id):
        """Deletes a group by it's ID
               ---
              tags:
              - Groups
              parameters:
                - name: group_id
                  in: path
                  schema:
                    type: integer
                  required: true
                  description: ID of the group that need to be deleted.
              responses:
                200:
                  description: OK
                404:
                  description: Not found
                505:
                  description: Internal server error
                                                   """
        with Session() as session:
            session.execute(delete(Group).filter(Group.id == group_id))
            session.commit()
            return f"successfully deleted group id:{group_id}"
