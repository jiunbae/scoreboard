from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app import Base

class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(128))
    content     = Column(Text)
    uid         = Column(Integer, ForeignKey('user.id'))

    user        = relationship("User", backref=backref('post', order_by=id))

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, content, uid):
        self.title = title
        self.content = content
        self.uid = uid

    def __repr__(self) -> str:
        return ','.join(map(str, [self.desc, self.file, self.aid, self.uid]))
