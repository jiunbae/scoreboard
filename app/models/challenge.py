from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app import app
from app import Base
from app.lib.file import File
from app.lib.metric import Metric

class Challenge(Base):
    __tablename__ = 'challenge'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    directory   = app.config['CHALLENGE_FOLDER']
    categories  = Metric.all()

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(64))
    desc        = Column(String(128))
    label       = Column(String(128))
    train       = Column(String(128))
    test        = Column(String(128))
    cate        = Column(Integer)
    start       = Column(DateTime)
    due         = Column(DateTime)
    submissions = relationship("Submission")

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, start, due, cate, desc, label, train='', test=''):
        if cate not in Challenge.categories:
            raise Exception("Wrong type")
        self.title = title
        self.start = start
        self.due = due
        self.cate = Challenge.categories.index(cate)
        self.desc = File(Challenge.directory).write(desc).name
        self.label = File(Challenge.directory).write(label).name
        self.train = File(Challenge.directory).write(train).name
        self.test = File(Challenge.directory).write(test).name

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.desc, self.cate, self.start, self.due]))
