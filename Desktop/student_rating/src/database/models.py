from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, String, Integer, Text, BOOLEAN, BINARY
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

from werkzeug.security import generate_password_hash

from src import db

Base = declarative_base()
Base.query = db.session.query_property()


def admin(email):
    if '@staff' in email:
        return True
    else:
        return False


def stud(email):
    if '@lpnu' in email:
        return True
    else:
        return False


class User(Base, UserMixin):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    email = Column(String(25), unique=True, nullable=False)
    password = Column(String(45), nullable=False)
    phone = Column(String(25), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)

    def __init__(self, username, first_name, last_name, email, password, phone):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.phone = phone
        self.is_admin = admin(email)
        self.is_student = stud(email)

    def get_id(self):
        return self.id_user

    def __repr__(self):
        return f'User( {self.id_user}, {self.username}, {self.first_name}, {self.last_name}, {self.email}, ' \
               f'{self.password}, {self.phone}, {self.is_student})'


class Student(Base):
    __tablename__ = 'student'
    id_student = Column(Integer, primary_key=True)
    name_student = Column(String(45), nullable=False)
    last_name_student = Column(String(45), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    rating = Column(String(45))
    id_user = Column(Integer, ForeignKey('user.id_user'), nullable=False)

    def __init__(self, name_student, last_name_student, rating, email, id_user):
        self.name_student = name_student
        self.last_name_student = last_name_student
        self.rating = rating
        self.email = email
        self.id_user = id_user

    def __repr__(self):
        return 'Student ' + str(
            self.id_student) + ' ' + self.name_student + ' ' + self.last_name_student + ' ' + self.email + '\n'


class Subject(Base):
    __tablename__ = 'subject'
    id_subject = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name_subject = Column(String(100), nullable=False, unique=True, )

    def __init__(self, id_subject, name_subject):
        self.id_subject = id_subject
        self.name_subject = name_subject

    def __repr__(self):
        return 'Subject ' + str(self.id_subject) + ' ' + self.name_subject + '\n'


class Mark(Base):
    __tablename__ = 'mark'

    id_mark = Column(Integer, primary_key=True, unique=True, )
    grade = Column(Integer, nullable=False)
    id_subject = Column(Integer, ForeignKey('subject.id_subject'), nullable=False)
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False)
    id_user = Column(Integer, ForeignKey('user.id_user'), nullable=False)

    def __init__(self, grade, id_subject, id_student, id_user):
        self.grade = grade
        self.id_subject = id_subject
        self.id_student = id_student
        self.id_user = id_user

    def __repr__(self):
        return 'Mark ' + str(self.grade) + ' ' + str(self.id_student) + ' ' + str(self.id_subject) + '\n'

    def to_dict(self):
        return {
            'id_student': self.id_student,
            'id_subject': self.id_subject,
            'grade': self.grade
        }
