from typing import Optional, List, Callable, Tuple
from functools import partial

from app import Base
from app import Session
from app.lib.file import File

class Controller:
    model = None

    @classmethod
    def index(cls, pack: bool = True, sort_by: Base = None, reverse: bool = True):
        result = Session.query(cls.model)
        if sort_by:
            result = result.order_by((getattr(sort_by, 'desc') if reverse else getattr(sort_by, 'asc'))())
        result = result.all()
        return result if not pack else Controller.package(result)

    @classmethod
    def create(cls, data: dict) -> Optional[Base]:
        try:
            instance = cls.model(**data)
            Session.add(instance)
            Session.commit()

            return instance
        except Exception as e:
            raise Exception(e)

    @classmethod
    def show(cls, id: int, pack: bool = False) -> Optional[Base]:
        try:
            result = Session.query(cls.model).get(id)
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
__all__ = list(import_subclass(__path__, Controller, locals()))

def default_params():
    return {'user': User.current()}
