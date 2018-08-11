from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from app.lib.utils import get_assignments, get_assignment

app = Flask(__name__)

# app config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'SECRET_KEY'

db = SQLAlchemy(app)

from app.models import *

db.create_all()
