from app import Session
from app.models import Assignment as model

class Assignment():
    @staticmethod
    def index():
        return [instance.__dict__ for instance in Session.query(model).all()]

    @staticmethod
    def create(data):
        Session.add(model(**data))
        Session.commit()

    @staticmethod
    def show(aid):
        try:
            return Session.query(model).get(aid)
        except:
            return None

    @staticmethod
    def destroy(aid):
        pass

