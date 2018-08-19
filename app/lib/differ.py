class Metric:
    pass

class Classification(Metric):
    @staticmethod
    def clac(tar, obj):
        return sum(all(trow.values[1:].argmax()+1 == orow.values[1:])
                    for (_, trow), (_, orow) in zip(tar.iterrows(), obj.iterrows()))

class MIOU(Metric):
    pass

class MAP(Metric):
    pass

import numpy as np
import pandas as pd

class Differ:
    def __init__(self, tar: str, obj: str, metric: Metric):
        self.tar = Differ.read(tar, index=None)
        self.obj = Differ.read(obj, index=None)
        self.metric = metric.calc

    @staticmethod
    def read(file: str):
        return pd.read_csv(file)

    def score(self) -> float:
        return self.metric(self.tar, self.obj)
