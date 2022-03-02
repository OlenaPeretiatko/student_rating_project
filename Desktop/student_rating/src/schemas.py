from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import User, Student, Mark

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        include_fk = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['id_user']
        load_instance = True

class MarkSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mark
        load_instance = True
        include_fk = True