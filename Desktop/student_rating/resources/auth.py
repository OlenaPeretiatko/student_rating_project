from flask import request, g, make_response, render_template, url_for
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from src import db, app
from src.database.models import User
from src.schemas import UserSchema

auth = HTTPBasicAuth()
headers = {'Content-Type': 'text/html'}

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'authlogin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


class AuthRegister(Resource):
    user_schema = UserSchema()

    def get(self):
        return make_response(render_template('register.html'), 200, headers)

    def post(self):
        try:
            user = User(
                username=request.form['username'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                password=request.form['password'],
                phone=request.form['phone'],
            )
            db.session.add(user)
            db.session.commit()
        # except ValidationError as e:
        #     # return make_response(render_template('notifications.html'), 200, headers)
        #     return {'message': str(e)}
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Such user exists'}, 409
        return make_response(render_template('register.html'), 200, headers)
        # return self.user_schema.dump(user)


class AuthLogin(Resource):
    def get(self):
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        print('post')
        username = request.form['username']
        password = request.form['password']
        print(username)
        user = db.session.query(User).filter_by(username=username).first()
        if verify_password(username, password):
            login_user(user)
            return make_response(render_template('profile.html', user=current_user), 200, headers)
        else:
            print(user)
            # return make_response(render_template('profile.html'), 401, headers)


class Profile(Resource):
    def get(self):
        return make_response(render_template('profile.html', user=current_user), 200, headers)


class AuthLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('default'))
        # if g.user:
        #     g.user = None
        #     return make_response(render_template('notifications.html', message="Successful logout"), 200, headers)
        # else:
        #     return make_response(render_template('notifications.html', message="Authorize to log out"), 401, headers)


@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False
    g.user = user
    return True
