# project/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from project.local_settings import SQLALCHEMY_DATABASE_URI
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

student_course = db.Table('student_course',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id', ondelete="CASCADE")),
                          db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete="CASCADE")))


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(15), unique=True)

    def __repr__(self):
        return f"id: {Group.id}, name: {Group.name}"


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(15))
    last_name = db.Column(String(15))
    group_id = db.Column(Integer, ForeignKey('group.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)

    course_rel = db.relationship("Course", secondary=student_course, back_populates='stud_rel', cascade='all, delete',
                                 lazy=True)

    def __repr__(self):
        return f"id: {Student.id}, first_name: {Student.first_name}, last_name: {Student.last_name}, group_id = {Student.group_id}"


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(15), unique=True)
    description = db.Column(String(250))

    stud_rel = db.relationship('Student', secondary=student_course, back_populates='course_rel', passive_deletes=True,
                               lazy=True)

    def __repr__(self):
        return f"id: {Course.id}, name: {Course.name}, description: {Course.description}"


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    db.metadata.drop_all(engine)
    db.metadata.create_all(engine)
