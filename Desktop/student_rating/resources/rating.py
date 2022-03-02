import json

from flask import render_template, make_response

from src.database.models import Student, Subject, Mark

from flask_restful import Resource
from marshmallow import ValidationError

from src import db

headers = {'Content-Type': 'text/html'}


class RatingListApi(Resource):
    def get(self, id_subject):
        try:
            subject = db.session.query(Subject).filter(Subject.id_subject == id_subject).first()
            mark = db.session.query(Mark.grade, Mark.id_student).filter(Mark.id_subject == id_subject).order_by(
                Mark.grade.desc()).all()
            students = []
            name_old = ''
            for i in mark:
                student = db.session.query(Student).filter(Student.id_student == i[1]).first()
                if not student:
                    return {'message': 'Student not found'}, 400
                if student.id_student == name_old:
                    continue
                student_data = {"id_student": student.id_student, "name_student": student.name_student,
                                "last_name_student": student.last_name_student,
                                "grade": ((str(i)).split('(')[1]).split(',')[0]}
                name_old = student.id_student
                students.append(student_data)
        except ValidationError as e:
            return {'message': str(e)}, 400
        if not students or not subject:
            return {'message': 'Student or subject not found'}, 400
        return make_response(render_template('student_rating.html', students=students), 200, headers)
