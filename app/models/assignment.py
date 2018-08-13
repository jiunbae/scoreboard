from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app import Base

class Assignment(Base):
    __tablename__ = 'assignment'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(64))
    content     = Column(Text)
    cate        = Column(Integer)
    start       = Column(DateTime)
    due         = Column(DateTime)
    submissions = relationship("submission")

    def __init__(self, id, title, content, cate, start, due):
        self.id = id
        self.title = title
        self.content = content
        self.cate = cate
        self.start = start
        self.due = due

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.content, self.cate, self.start, self.due]))

    def __dict__(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
