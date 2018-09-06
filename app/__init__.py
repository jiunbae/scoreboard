from os import makedirs
from flask import Flask

def create_app(config: dict) -> Flask:
    app = Flask(__name__)

    # app config
    app.secret_key = config['SECURE']['secret_key']
    app.config['RUN'] = config['RUN']
    app.config['PATH'] = PATH = config['PATH']
    try:
        for path in app.config['PATH']:
            makedirs(path)
    except OSError as e:
        pass

    # login manager
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # db connection
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    Engine      = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
                                config['DB']['user'],
                                config['DB']['pass'],
                                config['DB']['server'],
                                config['DB']['db']), convert_unicode=True)
    Session     = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=Engine))
    Base        = declarative_base()
    Base.query  = Session.query_property()

    # TODO: remove this trick
    globals().update(locals())

    from . import models
    from . import view

    Base.metadata.create_all(bind=Engine)

    return app
