from typing import List

from sqlalchemy import and_

from app import Session
from app import models
from app.controller import Controller

class Challenge(Controller):
    model = models.Challenge

    @classmethod
    def get_rankings(cls, cid: int) -> List[dict]:
        submissions = Session.query(models.Submission)\
                             .filter(and_(models.Submission.cid==cid,
                                          models.Submission.state=='done',
                                          models.Submission.result=='done'))\
                             .order_by(models.Submission.score.desc())\
                             .all()

        return [{
            'score': instance.score,
            'user': instance.user.studentid,
            'rank': rank,
        } for rank, instance in enumerate(submissions, 1)]
