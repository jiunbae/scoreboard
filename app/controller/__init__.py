from typing import Optional

from app import Base
from app import Session

class Controller:
    model = None

    @classmethod
    def index(cls):
        return [instance.__dict__ for instance in Session.query(cls.model).all()]

    @classmethod
    def create(cls, data: dict) -> Optional[Base]:
        try:
            instance = cls.model(**data)
            Session.add(instance)
            Session.commit()
            return instance
        except:
            return None

    @classmethod
    def show(cls, id: int) -> Optional[Base]:
        try:
            return Session.query(cls.model).get(id)
        except:
            return None

    @classmethod
    def destroy(cls, id: int) -> Optional[Base]:
        try:
            instance = cls.model.query.filter_by(id=id).one()
            Session.delete(instance)
            Session.commit()
            return instance
        except:
            return None

import glob
from os.path import dirname, basename, isfile

files = glob.glob(dirname(__file__) + "/*.py")
modules = map(basename, filter(lambda f: isfile(f) and not f.startswith('__'), files))
__all__ = list(map(lambda f: f.split('.')[0], modules))
from .assignment import Assignment
from .submission import Submission
from .user import User

def default_params():
    return {'user': User.current()}
