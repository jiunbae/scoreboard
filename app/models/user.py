from app import Base

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    studentid   = Column(String(12), unique=True)
    password    = Column(String(96))
    TA          = Column(Boolean)
    submissions = relationship("Submission")

    def __init__(self, studentid, password):
        self.studentid = studentid
        self.set_safe_password(password)

    def __repr__(self) -> str:
        return ','.join(map(str, [self.studentid, self.password]))

    def set_safe_password(self, password: str):
        self.password = generate_password_hash(password)

    def assert_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
