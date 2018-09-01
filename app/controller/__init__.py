from typing import Optional, List, Callable, Tuple, Any
from functools import partial

from app import Base
from app import Session
from app.lib.file import File

class Controller:
    model = None

    @classmethod
    def index(cls,
              filter_by: dict = None,
              sort_by: Base = None,
              reverse: bool = True,
              pack: bool = True) -> List[Base]:
        result = cls.model.query
        if filter_by:
            result = result.filter_by(**filter_by)
        if sort_by:
            result = result.order_by((getattr(sort_by, 'desc' if reverse else 'asc'))())
        result = result.all()
        return result if not pack else Controller.package(result)

    @classmethod
    def create(cls, data: dict) -> Optional[Base]:
        # try:
        instance = cls.model(**data)
        Session.add(instance)
        Session.commit()

        return instance
        # except Exception as e:
        #     raise Exception(e)

    @classmethod
    def show(cls, id:int, pack: bool = False) -> Optional[Base]:
        try:
            result = cls.model.query.get(id)
            return result if not pack else Controller.package(result)
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

    @staticmethod
    def package(elements: Tuple[Base, List[Base]]) -> Tuple[dict, List[dict]]:
        if isinstance(elements, list):
            return list(map(Controller.package, elements))
        return elements.__dict__

    @staticmethod
    def formatter(elements: Tuple[dict, List[dict]],\
                  target: Callable = lambda k, v: True,\
                  format: Callable = lambda v: v) -> Tuple[dict, List[dict]]:
        if isinstance(elements, list):
            return list(map(partial(Controller.formatter, target=target, format=format), elements))
        return {k: (format(v) if target(k, v) else v) for k, v in elements.items()}

from app.lib.moduletools import import_subclass
__all__ = list(map(lambda x: x.__name__, import_subclass(__path__, Controller, locals())))

# from app.controller.challenge import Challenge
# from app.controller.post import Post
# from app.controller.submission import Submission
# from app.controller.user import User

def default_params():
    return {'user': User.current()}
