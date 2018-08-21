import asyncio
from os.path import join
from uuid import uuid4
from typing import Optional

from app import app
from app import Handler
from app import Session
from app.controller import Controller
from app.models import Submission as submission


class Submission(Controller):
    model = submission

    @classmethod
    def create(cls, data: dict) -> Optional[submission]:
        # try:
        instance = cls.model(**data)
        Session.add(instance)
        Session.commit()

        Handler.scoring(instance)

        return instance
        # except:
        #     return None

    @classmethod
    def write_file(cls, file) -> None:
        filename = str(uuid4())
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        return filename

    @classmethod
    def get_file_path(cls, filename: str) -> str:
        return join(app.config['UPLOAD_FOLDER'], filename)
