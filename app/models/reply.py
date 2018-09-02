from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.models import Base

class Reply(Base):
    __tablename__ = 'reply'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = Column(Integer, primary_key=True, unique=True)
    content     = Column(Text)
    pid         = Column(Integer, ForeignKey('post.id'))
    uid         = Column(Integer, ForeignKey('user.id'))

    post        = relationship("Post", backref=backref('reply', order_by=id))
    user        = relationship("User", backref=backref('reply', order_by=id))

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, content, pid, uid):
        self.content = content
        self.pid = pid
        self.uid = uid

    def __repr__(self) -> str:
        return ','.join(map(str, [self.content, self.pid, self.uid]))
