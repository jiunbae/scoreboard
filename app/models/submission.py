from app import db

from datetime import datetime

class Submission(db.Model):
    __tablename__ = 'submission'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id      = db.Column(db.Integer, primary_key=True, unique=True)
    desc    = db.Column(db.String(128))
    file    = db.Column(db.String(128))
    aid     = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    uid     = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime)

    def __init__(self, id, desc, file, pid, uid):
        self.id = id
        self.desc = desc
        self.file = file
        self.aid = aid
        self.uid = uid

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.content, self.cate, self.start, self.due]))

    def __dict__(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
