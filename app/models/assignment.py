from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app import Base
from app.lib.metric import Metric

class Assignment(Base):
    __tablename__ = 'assignment'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    categories  = Metric.all()

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(64))
    file        = Column(String(128))
    label       = Column(String(128))
    cate        = Column(Integer)
    start       = Column(DateTime)
    due         = Column(DateTime)
    submissions = relationship("Submission")

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, file, label, cate, start, due):
        if cate not in Assignment.categories:
            raise Exception("Wrong type")
        self.title = title
        self.file = file
        self.label = label
        self.cate = Assignment.categories.index(cate)
        self.start = start
        self.due = due

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.file, self.cate, self.start, self.due]))
