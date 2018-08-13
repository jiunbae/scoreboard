from app import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    studentid   = Column(String(12))
    pw          = Column(String(32))
    submissions = relationship("Submission")

    def __init__(self, studentid, pw):
        self.studentid = studentid
        self.pw = pw

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.content, self.cate, self.start, self.due]))
