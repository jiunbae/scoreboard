from datetime import datetime
from collections import OrderedDict

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app import app
from app.models import Base
from app.lib.file import File
from app.lib.metric import Metric

class Challenge(Base):
    __tablename__ = 'challenge'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    directory   = app.config['CHALLENGE_FOLDER']
    categories  = Metric.all()
    board_roles = ['rank', 'user', 'score', 'time']

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(64))
    desc        = Column(String(128))
    label       = Column(String(128))
    train       = Column(String(128))
    test        = Column(String(128))
    cate        = Column(Integer)
    start       = Column(DateTime)
    due         = Column(DateTime)
    board_role  = Column(Integer)
    submissions = relationship("Submission")

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, start, due, cate, desc, label, train='', test=''):
        if cate not in self.categories:
            raise Exception("Wrong type")
        self.title = title
        self.start = start
        self.due = due
        self.board_role = 0
        self.cate = self.categories.index(cate)
        self.desc = File(self.directory).write(desc).name
        self.label = File(self.directory).write(label).name
        self.train = train and File(self.directory).write(train).name
        self.test = test and File(self.directory).write(test).name

    def roles(self) -> dict:
        role = bin(self.board_role)[2:].zfill(len(self.board_roles))[::-1]
        return OrderedDict([(name, role[i] == '0') for i, name in enumerate(self.board_roles)])

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.desc, self.cate, self.start, self.due, self.board_role]))
