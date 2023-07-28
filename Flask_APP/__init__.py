from flask import Flask
import face_recog.FRmain as fr
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] =  os.environ["DATABASE_URI"]


db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view= "login"

class VideoCamera(object):
    def __init__(self):
        fr.create()
    def __del__(self):
        fr.delete()
    def get_frame(self):
        return fr.scan()

from flask_app import routes
