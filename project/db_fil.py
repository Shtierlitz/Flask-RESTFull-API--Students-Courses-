# project/db_fil.py

from flask.cli import with_appcontext
from project.models import *
from sqlalchemy.orm.session import sessionmaker
import random as rand
from string import ascii_lowercase
import click


def name_generator() -> str:
    ascii_lst = [s for s in ascii_lowercase]
    return f"{rand.choice(ascii_lst)}{rand.choice(ascii_lst)}-{rand.randint(1, 9)}{rand.randint(1, 9)}"


Session = db.session


@click.command(name='fill_db')
@with_appcontext
def fill_db():
    db.engine.echo = True
    Session = db.session
    courses_dict = {'math': 'Special mathematics course for a gifted',
                    'biology': "Basic biological course",
                    'music': "Signing practice",
                    'ukr_lang': 'Spelling of patriotic teachings',
                    'eng_lang': 'Getting to know Western partners',
                    'history': 'The story of how grandfathers fought',
                    'Python': 'Best course ever',
                    'ethic': 'How not to screw up when working in a team',
                    'sociology': 'Distribution of humanitarian aid during the war',
                    'psychology': 'How to understand a mentor and not quarrel with him when you don’t '
                                  'understand anything'
                    }
    student_fname_lst = ['Jack', 'John', 'Silvia', 'Vivienna', 'Brianna', 'Igrerio', 'Joseph', 'Acara', 'Gretta',
                         'Michael', 'Bastila', 'Karth', 'George', 'Stephan', 'Canderous', 'Juhany', 'Jolie', 'Aayla',
                         'Ahsoka', 'Amilyn']

    student_lname_lst = ['Sparrow', 'Kennedy', 'Strange', 'Wood', 'Hoy', "Davydovskyi", 'Dredd', 'Rough', 'Turnberg',
                         'Jackson', 'Shan', 'Onasy', 'Lukas', 'Spilberg', 'Ordo', 'Chan', 'Bindo', 'Secura', 'Tano',
                         'Holdo']

    for s in range(10):
        with Session() as session:
            group = Group(name=name_generator())
            session.add(group)
            session.commit()

    for course in courses_dict:
        with Session() as session:
            course = Course(name=course, description=courses_dict[course])
            session.add(course)
            session.commit()

    for i in range(200):
        with Session() as session:
            student = Student(first_name=rand.choice(student_fname_lst), last_name=rand.choice(student_lname_lst))
            session.add(student)
            session.commit()

    with Session() as session:
        students = session.query(Student).all()
        groups = session.query(Group).all()
        rand.shuffle(groups)
        for group in groups:
            for _ in range(rand.randint(10, 30)):
                if not students:
                    break
                student = students.pop()
                student.group_id = group.id
                session.commit()

    with Session() as session:
        course = session.query(Course).all()
        for student in session.query(Student).all():
            for i in range(0, rand.randint(1, 3)):
                choise = rand.choice(course)
                if choise in student.course_rel:
                    break
                student.course_rel.append(choise)
        session.commit()


if __name__ == '__main__':
    fill_db()
