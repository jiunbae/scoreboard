from os import listdir
from os.path import join
from uuid import uuid4

class File:
    def __init__(self, dirname: str, name: str = ''):
        self.dirname = dirname
        self.name = name or File.get_safe_file_name(dirname)

    def write(self, file):
        file.save(join(self.dirname, self.name))
        return self

    def read(self, mode='r') -> str:
        with open(join(self.dirname, self.name), mode) as file:
            return file.read()

    @staticmethod
    def get_safe_file_name(dirname: str) -> str:
        files = listdir(dirname)
        while True:
            name = str(uuid4())
            if name not in files: break
        return name
