from typing import Optional

from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from app import Base
from app import Session
from app import login_manager
from app import models
from app.controller import Controller

class User(Controller):
    model = models.User

    @classmethod
    def current(cls) -> models.User:
        try:
            return current_user if current_user.is_authenticated else None
        except:
            return None

    @classmethod
    def login(cls, sid: int, pw: str) -> Optional[models.User]:
        try:
            instance = cls.model.query.filter_by(studentid=sid).one()
            if instance.assert_password(pw):
                login_user(instance)
                return instance
            else:
                raise Exception('Password not match!')
        except:
            raise Exception('Not registered!')

    @classmethod
    @login_required
    def logout(cls) -> None:
        logout_user()

    @classmethod
    @login_required
    def update(cls, old: str, new: str) -> bool:
        instance = cls.current()
        if not instance.assert_password(old):
            raise Exception('Password not matched')
        instance.set_safe_password(new)
        Session.commit()
        return instance

    @classmethod
    def require_permission(cls, func):
        @login_required
        def wrapper(*args, **kwargs):
            instance = cls.current()
            asserted = instance.assert_permission()
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def require_login(cls, func):
        @login_required
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    # attributes
    @classmethod
    @login_required
    def submissions(cls):
        instance = cls.current()
        return Controller.package(Session.query(models.Submission)\
                                         .filter(models.Submission.uid == instance.id)
                                         .order_by(models.Submission.id.desc())\
                                         .all())

@login_manager.user_loader
def load_user(uid):
    return User.show(uid)
