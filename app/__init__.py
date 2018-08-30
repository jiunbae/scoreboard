import json

from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
with open('config.json') as f:
    conf = json.load(f)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# app config
app.secret_key = conf['APP']['secret_key']
app.config['SUBMISSION_FOLDER'] = conf['APP']['submission_folder']
app.config['CHALLENGE_FOLDER'] = conf['APP']['challenge_folder']

# db
Engine      = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
                            conf['DB']['user'],
                            conf['DB']['pass'],
                            conf['DB']['server'],
                            conf['DB']['db']), convert_unicode=True)
Session     = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=Engine))
Base        = declarative_base()
Base.query  = Session.query_property()

from app.lib.handler import Handler
from app.models import *
from app.view import *

Base.metadata.create_all(bind=Engine)
