import asyncio
from typing import Optional

from app import Session
from app.controller import Controller
from app.models import Submission as submission
from app.lib.handler import Handler

class Submission(Controller):
    model = submission

    @classmethod
    def create(cls, data: dict) -> Optional[submission]:
        instance = super(Submission, cls).create(data)
        if instance:
            Handler.scoring(instance)
        return instance
