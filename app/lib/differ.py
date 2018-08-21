import numpy as np
import pandas as pd

class Differ:
    def __init__(self, tar: str, obj: str, metric):
        self.tar = Differ.read(tar)
        self.obj = Differ.read(obj)

        tar_size = np.size(self.tar, 0)
        obj_size = np.size(self.obj, 0)

        if tar_size != obj_size:
            raise Exception("instance number mismatach")

        self.instances = tar_size
        self.metric = metric.calc

    @staticmethod
    def read(file: str, index: bool = False) -> np.ndarray:
        return pd.read_csv(file).values[:, 1:]

    def score(self) -> float:
        return self.metric(self.tar, self.obj) / self.instances
