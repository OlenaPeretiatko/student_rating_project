import json

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from src.database.models import User
from src.schemas import UserSchema

from flask import request, g, render_template, make_response, jsonify, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src import db

headers = {'Content-Type': 'text/html'}


class UsersListApi(Resource):
    user_schema = UserSchema()

    @login_required
    def get(self, username=None):
        if not (current_user.is_admin or current_user.is_student):
            return {'message': 'Access denied'}, 409
        if current_user.is_admin:
            if not username:
                users = db.session.query(User).all()
                return make_response(render_template('users.html', users=users), 200, headers)
            # return self.user_schema.dump(users, many=True), 200
            user = db.session.query(User).filter_by(username=username).first()
        else:
            print(current_user.email)
            user = db.session.query(User).filter_by(email=current_user.email).first()
        if not user:
            return {'message': 'User not found'}, 404
        return make_response(render_template('user.html', user=user), 200, headers)
        # return self.user_schema.dump(user), 200


class EditUserListApi(Resource):
    user_schema = UserSchema()

    @login_required
    def get(self, username=None):
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 409
        if not username:
            users = db.session.query(User).all()
            return make_response(render_template('users.html', users=users), 200, headers)
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        return make_response(render_template('edit.html', user=user), 200, headers)

    @login_required
    def post(self, username=None):
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 409
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        try:
            user.username = request.form['username']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email']
            user.phone = request.form['phone']
        except ValidationError as e:
            return {'message': str(e)}, 400
        try:
            db.session.add(user)
            db.session.commit()
            # return make_response(render_template('users.html'), 200, headers)
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Username or email can`t be updated'}, 409
        return redirect(url_for('userslistapi'))


class DeleteUserListApi(Resource):
    user_schema = UserSchema()

    @login_required
    def post(self, username):
        if not (current_user.is_admin or current_user.is_student):
            return {'message': 'Access denied'}, 409
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('userslistapi'))
