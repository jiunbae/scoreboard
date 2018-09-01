from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app import app
from app.models import Base

class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    directory   = app.config['POST_FOLDER']
    categories  = ['notice', 'qna']

    id          = Column(Integer, primary_key=True, unique=True)
    title       = Column(String(128))
    content     = Column(Text)
    cate        = Column(Integer)
    uid         = Column(Integer, ForeignKey('user.id'))
    replies     = relationship("Reply")

    user        = relationship("User", backref=backref('post', order_by=id))

    time_created= Column(DateTime(timezone=True), server_default=func.now())
    time_updated= Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, content, cate, uid):
        if cate not in self.categories:
            raise Exception('Unkown post category')
        self.title = title
        self.content = content
        self.uid = uid
        self.notice = self.categories.index(cate)

    def __repr__(self) -> str:
        return ','.join(map(str, [self.desc, self.file, self.aid, self.uid]))
