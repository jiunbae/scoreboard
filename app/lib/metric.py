import numpy as np 
from numpy import apply_along_axis as npa

class Metric:
    @classmethod
    def calc(cls, tar, obj):
        """ Metric for assignment submission

            return score
        """
        pass

    @classmethod
    def all(cls):
        return [klass.__name__.split('.')[-1] for klass in cls.__subclasses__()]

class Classification(Metric):
    @classmethod
    def calc(cls, tar: np.ndarray, obj: np.ndarray) -> int:
        result = npa(lambda r: np.argmax(r), 1, tar)
        return np.sum(result == np.subtract(obj, 1).T)

class mIOU(Metric):
    @classmethod
    def calc(cls, tar: np.ndarray, obj: np.ndarray) -> int:
        pass

class mAP(Metric):
    @classmethod
    def calc(cls, tar: np.ndarray, obj: np.ndarray) -> int:
        pass
