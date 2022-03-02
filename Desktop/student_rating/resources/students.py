from flask_login import login_required, current_user
from sqlalchemy import update
from werkzeug.utils import redirect

from src.database.models import Student, stud
from src.schemas import StudentSchema

from flask import request, g, make_response, render_template, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src import db


headers = {'Content-Type': 'text/html'}


class StudentListApi(Resource):
    student_schema = StudentSchema()

    @login_required
    def get(self, id_student=None):
        if not (current_user.is_admin or current_user.is_student):
            return {'message': 'Access denied'}, 409
        if current_user.is_admin:
            if not id_student:
                students = db.session.query(Student).all()
                return make_response(render_template('students.html', students=students), 200, headers)
            else:
                student = db.session.query(Student).filter_by(id_student=id_student).first()
                return make_response(render_template('students.html', students=[student]), 200, headers)
        else:
            student = db.session.query(Student).filter_by(email=current_user.email).first()
        if not student:
            return {'message': 'Student not found'}, 404
        return make_response(render_template('students.html', students=[student]), 200, headers)


class AddStudentListApi(Resource):
    student_schema = StudentSchema()

    @login_required
    def get(self):
        return make_response(render_template('addStudent.html'), 200, headers)

    @login_required
    def post(self):
        if not current_user.is_admin:
            return {'message': 'Access denied'}, 409
        try:
            student = Student(
                name_student=request.form['name_student'],
                last_name_student=request.form['last_name_student'],
                rating=request.form['rating'],
                email=request.form['email'],
                id_user=request.form['id_user']
            )
            if current_user.id_user != student.id_user:
                return make_response(render_template('notifications.html',
                                                     message="Sorry, you can not mark this student"), 400, headers)
            else:
                db.session.add(student)
                db.session.commit()
        except ValidationError as e:
            return make_response(render_template('notifications.html'), 200, headers)
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Such user exists'}, 409
        return redirect(url_for('studentlistapi'))


class EditStudentListApi(Resource):
    student_schema = StudentSchema()

    # def get(self, id_student=None):
    #     if not id_student:
    #         students = db.session.query(Student).all()
    #         print(students)
    #         return make_response(render_template('students.html', students=students), 200, headers)
    #     student = db.session.query(Student).filter_by(id_student=id_student).first()
    #     print(student)
    #     if not student:
    #         return {'message': 'User not found'}, 404
    #     return make_response(render_template('editStudent.html', student=student), 200, headers)
    #
    # # @auth.login_required()
    # def post(self, id_student=None):
    #     # if not current_user.is_admin and current_user.username != username:
    #     #     return {'message': 'Access denied'}, 409
    #     student = db.session.query(Student).filter_by(id_student=id_student).first()
    #     print(student)
    #     if not student:
    #         return {'message': 'User not found'}, 404
    #     try:
    #         student_updated = Student(
    #             name_student=request.form['name_student'],
    #             last_name_student=request.form['last_name_student'],
    #             email=request.form['email'],
    #             rating='1',
    #             id_user=1,
    #         )
    #     except ValidationError as e:
    #         return {'message': str(e)}, 400
    #     try:
    #         db.session.delete(student)
    #         db.session.add(student_updated)
    #         db.session.commit()
    #         # return make_response(render_template('users.html'), 200, headers)
    #     except IntegrityError:
    #         db.session.rollback()
    #         return {'message': 'Username or email can`t be updated'}, 409
    #     return redirect(url_for('studentlistapi'))

    @login_required
    def get(self, id_student=None):
        if not (current_user.is_admin or current_user.is_student):
            return {'message': 'Access denied'}, 409
        if current_user.is_admin:
            if not id_student:
                students = db.session.query(Student).all()
                return make_response(render_template('students.html', students=students), 200, headers)
                # return self.student_schema.dump(students, many=True), 200
            student = db.session.query(Student).filter_by(id_student=id_student).first()
        else:
            student = db.session.query(Student).filter_by(email=current_user.email).first()
        if not student:
            return {'message': 'Student not found'}, 404
        return make_response(render_template('editStudent.html', student=student), 200, headers)

    @login_required
    def post(self, id_student):
        if not current_user.is_admin:
            return {'message': 'Access denied'}, 409
        student = db.session.query(Student).filter_by(id_student=id_student).first()
        if not student:
            return {'message': 'Student not found'}, 404
        try:
            student.name_student = request.form['name_student']
            student.last_name_student = request.form['last_name_student']
            student.email = request.form['email']
        except ValidationError as e:
            return {'message': str(e)}, 400
        if stud(student.email) is False:
            return {'message': 'You can not update this student'}, 409
        try:
            db.session.add(student)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Such student exists'}, 409
        return redirect(url_for('studentlistapi'))


class DeleteStudentListApi(Resource):
    student_schema = StudentSchema()

    @login_required
    def post(self, id_student):
        if not current_user.is_admin:
            return {'message': 'Access denied'}, 409
        student = db.session.query(Student).filter_by(id_student=id_student).first()
        if not student:
            return "Student not found", 400
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('studentlistapi'))
        # return "Successfully deleted", 20
