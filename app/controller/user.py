from typing import Optional

from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from app import Base
from app import Session
from app import login_manager
from app.controller import Controller
from app.models import User as user

class User(Controller):
    model = user

    @classmethod
    @login_required
    def current(cls) -> user:
        return current_user

    @classmethod
    def login(cls, sid: int, pw: str) -> Optional[Base]:
        try:
            instance = cls.model.query.filter_by(studentid=sid).filter_by(password=pw).one()
            login_user(instance)
            return instance
        except:
            return None

    @classmethod
    @login_required
    def logout(cls) -> None:
        logout_user()

@login_manager.user_loader
def load_user(uid):
    return User.show(uid)
