from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# app config
app.secret_key = 'SECRET_KEY'

# db
Engine      = create_engine('mysql+pymysql://root@localhost/test?charset=utf8', convert_unicode=True)
Session     = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=Engine))
Base        = declarative_base()
Base.query  = Session.query_property()

from app.models import *
from app.view import *

Base.metadata.create_all(bind=Engine)
