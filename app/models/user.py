from app import Base

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    studentid   = Column(String(12))
    password    = Column(String(32))
    submissions = relationship("Submission")

    def __init__(self, studentid, password):
        self.studentid = studentid
        self.password = password

    def __repr__(self) -> str:
        return ','.join(map(str, [self.studentid, self.password]))
