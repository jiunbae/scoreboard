from typing import Tuple

import numpy as np 
from numpy import apply_along_axis as npa
from sklearn.metrics import average_precision_score

class Metric:
    def __call__(self, tar: np.ndarray, obj: np.ndarray) -> float:
        return 0

    @staticmethod
    def normalize(size: int, result: Tuple[float, int]) -> float:
        return result / size

    @classmethod
    def all(cls):
        return [klass.__name__.split('.')[-1] for klass in cls.__subclasses__()]

class Classification(Metric):
    def __call__(self, tar: np.ndarray, obj: np.ndarray) -> float:
        result = npa(lambda r: np.argmax(r), 1, tar[:, 1:])
        return (np.add(result, 1) == obj[:, 1:].squeeze()).mean()

class mIOU(Metric):
    def __call__(self, tar: np.ndarray, obj: np.ndarray) -> float:
        result = npa(mIOU.overlap, 1, np.column_stack((tar[:, 1:], obj[:, 1:]))).mean()
        return result

    @staticmethod
    def overlap(row):
        tarL, tarT, tarW, tarH, objL, objT, objW, objH = row
        left = np.maximum(np.maximum(0, tarL), np.maximum(0, objL))
        right = np.minimum(tarL + tarW, objL + objW)
        top = np.maximum(np.maximum(0, tarT), np.maximum(0, objT))
        bottom = np.minimum(tarT + tarH, objT + objH)
        intersect = np.maximum(0, right - left) * np.maximum(0, bottom - top)
        intersect = 0 if intersect < 0 else intersect
        union = tarW * tarH + objW * objH - intersect
        return np.clip(intersect / union, 0, 1)

class mAP(Metric):
    def __call__(self, tar: np.ndarray, obj: np.ndarray) -> float:
        result = npa(mAP.precision, 1, np.column_stack((tar[:, 1:], obj[:, 1:]))).mean()
        return Metric.normalize(np.size(tar, 0), result)

    @staticmethod
    def precision(row):
        (y_true, y_score) = row
        return average_precision_score(y_true, y_score)
