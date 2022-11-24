from project.app import *
from .fill_db_tests import fill_db_test
from project.models import *
from project.secondary_functions.scripts import *
import pytest


@pytest.fixture()
def app():
    app = create_app('testing')
    with app.app_context():
        fill_db_test(db)

        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_QueryGroups(client):
    # get
    response_get = client.get("/api/v1/groups")
    js = response_get.get_json()
    assert response_get.status_code == 200
    assert len(js) == 10
    assert {"id": 1, "name": "co-36"} in js
    assert {"id": 2, "name": "vs-89"} in js
    assert {"id": 3, "name": "bk-69"} in js
    assert {"id": 4, "name": "lo-19"} in js

    # post
    name = 'ts-44'
    response_post = client.post("/api/v1/groups", data=dict(name=name))
    assert response_post.status_code == 200
    response_get = client.get("/api/v1/groups")
    assert b'ts-44' in response_get.data


def test_QueryGroup(client):
    # get
    response_get = client.get("/api/v1/groups/1")
    assert response_get.status_code == 200
    assert b"co-36" in response_get.data

    # put
    group_name = "qq-11"
    response_put = client.put("api/v1/groups/1", data=dict(group_name=group_name))
    assert response_put.status_code == 200
    response_get = client.get("/api/v1/groups/1")
    assert b'qq-11' in response_get.data

    # delete
    response_delete = client.delete("api/v1/groups/1")
    assert response_delete.status_code == 200
    response_get = client.get("/api/v1/groups/1")
    assert response_get.status_code == 404


def test_QueryStudents(client):
    # get
    response_get = client.get("/api/v1/students")
    assert response_get.status_code == 200
    js = response_get.get_json()
    assert {'id': 1, 'first_name': 'Jack', 'last_name': 'Sparrow', 'group_id': 2} in js
    assert {'id': 2, 'first_name': 'John', 'last_name': 'Kennedy', 'group_id': 2} in js
    assert {'id': 6, 'first_name': 'Igrerio', 'last_name': 'Davydovskyi', 'group_id': 2} in js
    assert {'id': 7, 'first_name': 'Joseph', 'last_name': 'Dredd', 'group_id': 2} in js

    # post
    first_name = 'Robert'
    last_name = 'Polson'
    response_post = client.post("/api/v1/students", data=dict(first_name=first_name, last_name=last_name))
    assert response_post.status_code == 200
    response_get = client.get("/api/v1/students")
    js = response_get.get_json()
    assert {'id': 21, 'first_name': 'Robert', 'last_name': 'Polson', 'group_id': None} in js


def test_QueryStudent(client):
    # get
    response_get = client.get("/api/v1/students/2")
    assert response_get.status_code == 200
    js = response_get.get_json()
    assert {'id': 2, 'first_name': 'John', 'last_name': 'Kennedy', 'group_id': 2} in js

    # put
    first_name = 'Jose'
    last_name = 'Barera'
    response_put = client.put("/api/v1/students/2", data=dict(first_name=first_name, last_name=last_name))
    assert response_put.status_code == 200
    response_get = client.get("/api/v1/students/2")
    js = response_get.get_json()
    assert {'id': 2, 'first_name': 'Jose', 'last_name': 'Barera', 'group_id': 2} in js

    # delete
    response_delete = client.delete("/api/v1/students/2")
    assert response_delete.status_code == 200
    response_get = client.get("/api/v1/students/2/student")
    assert response_get.status_code == 404


def test_QueryStudentsCourses(client):
    # put
    response_put = client.post("/api/v1/courses/3/students/13")
    assert response_put.status_code == 200
    with db.session() as session:
        stud = session.query(Student).filter(Student.id == 13).first()
        assert {'id': 3, 'name': 'music', 'description': 'Signing practice'} in query_courses(stud.course_rel)

    # delete
    response_delete = client.delete("/api/v1/courses/3/students/13")
    assert response_delete.status_code == 200
    with db.session() as session:
        stud = session.query(Student).filter(Student.id == 13).first()
        assert {'id': 3, 'name': 'music', 'description': 'Signing practice'} not in query_courses(stud.course_rel)


def test_QueryStudentCourse(client):
    # get
    response_get = client.get("/api/v1/students/psychology/courses")
    assert response_get.status_code == 200
    js = response_get.get_json()
    assert {'id': 10, 'first_name': 'Michael', 'last_name': 'Jackson', 'group_id': 2} in js
    assert {'id': 11, 'first_name': 'Bastila', 'last_name': 'Shan', 'group_id': 1} in js
    assert {'id': 6, 'first_name': 'Igrerio', 'last_name': 'Davydovskyi', 'group_id': 2} in js


def test_QueryCourses(client):
    # get
    response_get = client.get("/api/v1/courses")
    assert response_get.status_code == 200
    js = response_get.get_json()
    assert {'id': 1, 'name': 'math', 'description': 'Special mathematics course for a gifted'} in js
    assert {'id': 10, 'name': 'psychology',
            'description': 'How to understand a mentor and not quarrel with him when you don’t understand anything'} in js
    assert {'id': 7, 'name': 'Python', 'description': 'Best course ever'} in js

    # post
    course_name = 'test'
    description = 'test_description'
    response_post = client.post("/api/v1/courses", data=dict(course_name=course_name, description=description))
    assert response_post.status_code == 200
    response_get = client.get("/api/v1/courses")
    js = response_get.get_json()
    assert {'id': 11, 'name': 'test', 'description': 'test_description'} in js


def test_QueryCourse(client):
    # get
    response_get = client.get("/api/v1/courses/10?course_name=test&description=test_description")
    assert response_get.status_code == 200
    js = response_get.get_json()
    assert {'id': 10, 'name': 'psychology',
            'description': 'How to understand a mentor and not quarrel with him when you don’t understand anything'} in js

    # put
    course_name = 'test'
    description = 'test_description'
    response_put = client.put("/api/v1/courses/10", data=dict(course_name=course_name, description=description))
    assert response_put.status_code == 200
    with db.session() as session:
        query = session.query(Course).filter(Course.id == 10, Course.name == "test").all()
        assert {'id': 10, 'name': 'test', 'description': 'test_description'} in query_courses(query)

    # delete
    response_delete = client.delete("/api/v1/courses/10")
    assert response_delete.status_code == 200
    response_get = client.get("/api/v1/courses/10")
    assert response_get.status_code == 404
