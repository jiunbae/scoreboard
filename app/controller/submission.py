import asyncio
from typing import Optional

from app import Session
from app import models
from app.controller import Controller
from app.lib.handler import Handler

class Submission(Controller):
    model = models.Submission

    @classmethod
    def create(cls, data: dict) -> Optional[models.Submission]:
        instance = super(Submission, cls).create(data)
        if instance:
            Handler.scoring(instance)
        return instance
