from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
import os


UPLOAD_FOLDER = os.path.join("static", "images")
IMAGE_ALLOWED_EXTENSIONS = {"jpg", "jpeg", "gif", "png"}
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
MAX_CONTENT_SIZE= 25 * 1000 * 1000 # 25 Megabytes

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_SIZE"] = MAX_CONTENT_SIZE
db = SQLAlchemy(app)
api = Api(app)