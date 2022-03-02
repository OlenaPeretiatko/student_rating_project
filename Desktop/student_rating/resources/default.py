from flask_restful import Resource
from flask import render_template, make_response
from marshmallow import ValidationError

from src import db
from src.database.models import Mark, Subject, Student

headers = {'Content-Type': 'text/html'}


class Default(Resource):
    def get(self):
        subjects = db.session.query(Subject).all()
        subjects_dict = {}
        for subject in subjects:
            subjects_dict[str(subject).split(' ')[1]] = (str(subject).split(' ')[2]).split('\n')[0]
        return make_response(render_template('index.html', subjects_dict=subjects_dict),
                             200, headers)
