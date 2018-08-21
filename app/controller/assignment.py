from os.path import join
from uuid import uuid4

from sqlalchemy import and_

from app import app
from app import Session
from app.controller import Controller
from app.models import Assignment as assignment
from app.models import Submission as submission

class Assignment(Controller):
    model = assignment

    @classmethod
    def write_file(cls, file: str) -> None:
        filename = str(uuid4())
        file.save(join(app.config['ASSIGNMENT_FOLDER'], filename))
        return filename

    @classmethod
    def get_file_path(cls, filename: str) -> str:
        return join(app.config['ASSIGNMENT_FOLDER'], filename)

    @classmethod
    def get_rankings(cls, aid: int):
        submissions = Session.query(submission)\
                          .filter(and_(submission.aid==aid,
                                       submission.state=='done',
                                       submission.result=='done'))\
                          .order_by(submission.score.desc())\
                          .all()

        return [{
            'score': instance.score,
            'user': instance.user.studentid,
            'rank': rank,
        } for rank, instance in enumerate(submissions, 1)]
