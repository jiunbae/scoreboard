from typing import List

from sqlalchemy import and_

from app import Base
from app import Session
from app import models
from app.controller import Controller

class Challenge(Controller):
    model = models.Challenge

    @classmethod
    def update(cls, cid: int, data: dict) -> Base:
        instance = Challenge.show(cid)
        if 'board_role' in data:
            base = list(reversed(list(map(int, '{0:0b}'.format(instance.board_role)))))
            value = data.get('board_role', 0)
            if len(base) <= abs(value):
                instance.board_role += pow(2, abs(value)) * (value/abs(value))
            elif base[abs(value)] == value > 0:
                raise Exception('role already checked/unchecked')
            else:
                instance.board_role += pow(2, abs(value)) * (value/abs(value))
        Session.commit()
        return instance

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
