from sqlalchemy import and_

from app import Session
from app.controller import Controller
from app.models import Challenge as challenge
from app.models import Submission as submission

class Challenge(Controller):
    model = challenge

    @classmethod
    def get_rankings(cls, cid: int):
        submissions = Session.query(submission)\
                             .filter(and_(submission.cid==cid,
                                          submission.state=='done',
                                          submission.result=='done'))\
                             .order_by(submission.score.desc())\
                             .all()

        return [{
            'score': instance.score,
            'user': instance.user.studentid,
            'rank': rank,
        } for rank, instance in enumerate(submissions, 1)]
