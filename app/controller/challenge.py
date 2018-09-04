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
            base = list(map(int, '0'+bin(instance.board_role)[2:].zfill(len(cls.model.board_roles))[::-1]))
            value = data.get('board_role')
            base[abs(value)] = int(value > 0)
            instance.board_role = int(''.join(map(str, base[1:][::-1])), 2)
        Session.commit()
        return instance

    @classmethod
    def get_rankings(cls, cid: int) -> List[dict]:
        role = Challenge.show(cid).roler()
        submissions = Session.query(models.Submission)\
                             .filter(and_(models.Submission.cid==cid,
                                          models.Submission.state=='done',
                                          models.Submission.result=='done'))\
                             .order_by(models.Submission.score.desc())\
                             .all()
        result = [{
            'rank': rank,
            'score': instance.score,
            'user': instance.user.studentid,
            'time': instance.time_created.strftime('%B %d, %H:%M'),
        } for rank, instance in enumerate(submissions, 1)]

        # bluer
        return list(map(lambda i: { k: v if role[k] else '###' for k, v in i.items()}, result))
