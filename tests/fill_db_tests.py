from project.models import *



def fill_db_test(db):
    # db.engine.echo = True
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

    group_list = ['co-36', 'vs-89', 'bk-69', 'lo-19', 'vv-83', 'uy-24', 'wf-69', 'xl-82', 'ay-14', 'hl-64']


    for s in range(len(group_list)):
        with Session() as session:
            group = Group(name=group_list[s])
            session.add(group)
            session.commit()

    for course in courses_dict:
        with Session() as session:
            c = Course(name=course, description=courses_dict[course])
            session.add(c)
            session.commit()

    for i in range(len(student_fname_lst)):
        with Session() as session:
            student = Student(first_name=student_fname_lst[i], last_name=student_lname_lst[i])
            session.add(student)
            session.commit()

    with Session() as session:
        students = session.query(Student).all()
        groups = session.query(Group).all()

        for group in groups:
            for _ in range(10):
                if not students:
                    break
                student = students.pop()
                student.group_id = group.id
                session.commit()

    with Session() as session:
        course = session.query(Course).all()
        for student in session.query(Student).all():
            for i in range(len(courses_dict)):
                choise = course[i]
                student.course_rel.append(choise)
        session.commit()

# if __name__ == '__main__':
#     fill_db()
