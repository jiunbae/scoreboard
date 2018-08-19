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
    def current(cls) -> user:
        return current_user if current_user.is_authenticated else None

    @classmethod
    def login(cls, sid: int, pw: str) -> Optional[Base]:
        try:
            instance = cls.model.query.filter_by(studentid=sid).one()
            if instance.assert_password(pw):
                login_user(instance)
                return instance
            else:
                # case password not matched
                return None
        except:
            # case not registered
            return None

    @classmethod
    @login_required
    def logout(cls) -> None:
        logout_user()

    @classmethod
    def update(cls, pw: str) -> bool:
        instance = cls.current()
        print (instance, pw)
        if instance.assert_password(pw):
            print (instance.password)
            instance.set_safe_password(pw)
            print (instance.password)
            Session.add(instance)
            Session.commit()
            return instance
        return None

@login_manager.user_loader
def load_user(uid):
    return User.show(uid)
