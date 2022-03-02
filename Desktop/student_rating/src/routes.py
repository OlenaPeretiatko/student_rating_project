from flask import render_template

from resources.auth import AuthRegister, AuthLogin, AuthLogout, Profile
from resources.default import Default
from resources.marks import MarkListApi, AllMarksListApi, DeleteMarkListApi
from resources.rating import RatingListApi
from resources.students import StudentListApi, DeleteStudentListApi, EditStudentListApi, AddStudentListApi
from resources.users import UsersListApi, EditUserListApi, DeleteUserListApi
from src import api

api.add_resource(Default, '/', strict_slashes=False)

api.add_resource(UsersListApi, '/users', '/users/<username>', strict_slashes=False)
api.add_resource(EditUserListApi, '/edit', '/edit/<username>', strict_slashes=False)
api.add_resource(DeleteUserListApi, '/delete', '/delete/<username>', strict_slashes=False)

api.add_resource(StudentListApi, '/students', '/students/<id_student>', strict_slashes=False)
api.add_resource(AddStudentListApi, '/addStudent', strict_slashes=False)
api.add_resource(DeleteStudentListApi, '/deleteStudent', '/deleteStudent/<id_student>', strict_slashes=False)
api.add_resource(EditStudentListApi, '/editStudent', '/editStudent/<id_student>', strict_slashes=False)

api.add_resource(MarkListApi, '/mark', '/mark/<id_student>', strict_slashes=False)
api.add_resource(AllMarksListApi, '/allMarks', '/allMarks/<id_student>', strict_slashes=False)
api.add_resource(DeleteMarkListApi, '/deleteMark', '/deleteMark/<id_mark>', strict_slashes=False)

api.add_resource(RatingListApi, '/university/<id_subject>', strict_slashes=False)

api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(Profile, '/profile', '/profile/<username>', strict_slashes=False)
api.add_resource(AuthLogout, '/logout', strict_slashes=False)
