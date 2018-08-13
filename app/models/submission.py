from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import Base

class Submission(Base):
    __tablename__ = 'submission'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id      = Column(Integer, primary_key=True, unique=True)
    desc    = Column(String(128))
    file    = Column(String(128))
    aid     = Column(Integer, ForeignKey('assignment.id'))
    uid     = Column(Integer, ForeignKey('user.id'))

    user    = relationship("User", backref=backref('submission', order_by=id))

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
