from flask_login import LoginManager

from src import db, app
from src.database.models import User
from src.database.models import Subject
from src.database.models import Student
from src.database.models import Mark


def populate_db():
    user_1 = User(
        username='user1',
        first_name='User',
        last_name='User',
        email='user1@gmail.com',
        password='user1',
        phone='1111',
    )
    user_2 = User(
        username='user2',
        first_name='User',
        last_name='User',
        email='user2@gmail.com',
        password='user2',
        phone='1111',
    )
    user_3 = User(
        username='teacher',
        first_name='Teacher',
        last_name='Teacher',
        email='teacher@staff',
        password='teacher',
        phone='1111',
    )
    user_4 = User(
        username='student',
        first_name='Student',
        last_name='Student',
        email='student@lpnu',
        password='student',
        phone='1111',
    )
    subject_1 = Subject(
        id_subject=1,
        name_subject='Math'
    )
    subject_2 = Subject(
        id_subject=2,
        name_subject='English'
    )
    subject_3 = Subject(
        id_subject=3,
        name_subject='Psychology'
    )
    student_1 = Student(
        name_student='Oksana',
        last_name_student='Vorobel',
        rating='25',
        email='oksana@lpnu',
        id_user=3)

    student_2 = Student(
        name_student='Yulia',
        last_name_student='Zanevych',
        rating='30',
        email='yulia@lpnu',
        id_user=3
    )
    student_3 = Student(
        name_student='Emilia',
        last_name_student='Bondarenko',
        rating='30',
        email='emili@lpnu',
        id_user=3
    )
    mark_1 = Mark(
        grade=2,
        id_subject=2,
        id_student=1,
        id_user=3
    )
    mark_2 = Mark(
        grade=5,
        id_subject=2,
        id_student=2,
        id_user=3
    )
    mark_3 = Mark(
        grade=5,
        id_subject=3,
        id_student=2,
        id_user=3
    )
    mark_4 = Mark(
        grade=4,
        id_subject=1,
        id_student=3,
        id_user=3
    )
    mark_5 = Mark(
        grade=5,
        id_subject=1,
        id_student=2,
        id_user=3
    )

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)

    db.session.add(subject_1)
    db.session.add(subject_2)
    db.session.add(subject_3)

    db.session.add(student_1)
    db.session.add(student_2)
    db.session.add(student_3)

    db.session.add(mark_1)
    db.session.add(mark_2)
    db.session.add(mark_3)
    db.session.add(mark_4)
    db.session.add(mark_5)

    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    print('Populating db...')
    populate_db()

    print('Successfully populated!')
