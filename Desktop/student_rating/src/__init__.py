import config
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': 'Pharmacy'
#     }
# )
# app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
#

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')


from src import routes
from src.database import models
