import json
from sqlite3 import IntegrityError

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from src.database.models import User, Student, Subject, Mark
from src.schemas import MarkSchema

from flask import request, g, make_response, render_template, url_for
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from resources.auth import auth

headers = {'Content-Type': 'text/html'}


class AllMarksListApi(Resource):
    mark_schema = MarkSchema()

    @login_required
    def get(self, id_student=None):
        if not id_student:
            marks = db.session.query(Mark).all()
        else:
            marks = db.session.query(Mark).filter_by(id_student=id_student).all()

        full_names = []
        subjects = []
        teachers = []
        for el in marks:
            student = db.session.query(Student).filter_by(id_student=el.id_student).first()
            subject = db.session.query(Subject).filter_by(id_subject=el.id_subject).first()
            teacher = db.session.query(User).filter_by(id_user=el.id_user).first()
            full_names.append(student.name_student + ' ' + student.last_name_student)
            subjects.append(subject.name_subject)
            teachers.append(teacher.email)

        if not marks:
            return make_response(render_template('notifications.html', message="No marks"), 400, headers)

        return make_response(render_template('allMarks.html',
                                             marks=self.mark_schema.dump(marks, many=True),
                                             full_names=full_names,
                                             subjects=subjects,
                                             teachers=teachers,
                                             student=student), 200, headers)


class MarkListApi(Resource):
    mark_schema = MarkSchema()

    @login_required
    def get(self, id_student=None):
        if not (current_user.is_admin or current_user.is_student):
            return {'message': 'Access denied'}, 409
        if current_user.is_admin:
            if id_student:
                student = db.session.query(Student).filter_by(id_student=id_student).first()
                if not student:
                    return make_response(render_template('notifications.html', message="Student not found"), 400,
                                         headers)
                full_name = student.name_student + ' ' + student.last_name_student
                mark = db.session.query(Mark).filter_by(id_student=id_student).first()
                if not mark:
                    return make_response(render_template('notifications.html', message="Student not found"), 400,
                                         headers)
                return make_response(
                    render_template('mark.html', full_name=full_name, mark=self.mark_schema.dump(mark)),
                    200, headers)
            if not id_student:
                return make_response(render_template('notifications.html', message="Try again"), 400, headers)
        else:
            return make_response(render_template('notifications.html', message="Error"), 400, headers)


    @login_required
    def post(self, id_student=None):
        print(current_user)
        try:
            mark = Mark(
                grade=request.form['grade'],
                id_subject=request.form['id_subject'],
                id_student=id_student,
                id_user=request.form['id_user']
            )
            subject = db.session.query(Subject).filter_by(id_subject=mark.id_subject).first()
            user = db.session.query(User).filter_by(id_user=mark.id_user).first()
            if not subject:
                return make_response(render_template('notifications.html', message="SORRY, NO SUCH SUBJECT"), 400, headers)
            if not user:
                return make_response(render_template('notifications.html', message="SORRY, NO SUCH USER"), 400, headers)
            else:
                db.session.add(mark)
                db.session.commit()
            print(mark)
        except IntegrityError:
            db.session.rollback()
            return make_response(render_template('notifications.html', message="Such user exists"), 409, headers)
        return make_response(render_template('register.html'), 200, headers)


class DeleteMarkListApi(Resource):
    mark_schema = MarkSchema()

    @login_required
    def post(self, id_mark):
        if not current_user.is_admin:
            return {'message': 'Access denied'}, 409
        mark = db.session.query(Mark).filter_by(id_mark=id_mark).first()
        print(mark)
        if not mark:
            return "Student not found", 400
        db.session.delete(mark)
        db.session.commit()
        return redirect(url_for('allmarkslistapi'))
        # return "Successfully deleted", 20
