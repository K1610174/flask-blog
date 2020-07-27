from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('DATABASE_URI'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = str(os.getenv('SECRET_KEY'))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application import routes
