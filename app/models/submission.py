from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app import app
from app.models import Base
from app.lib.file import File

class Submission(Base):
    __tablename__ = 'submission'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    directory   = app.config['SUBMISSION_FOLDER']

    id          = Column(Integer, primary_key=True, unique=True)
    desc        = Column(String(128))
    file        = Column(String(128))
    cid         = Column(Integer, ForeignKey('challenge.id'))
    uid         = Column(Integer, ForeignKey('user.id'))

    state       = Column(String(16), default='submit')
    score       = Column(Float, default=.0)
    result      = Column(String(128), default='')

    user        = relationship("User", backref=backref('submission', order_by=id))
    challenge   = relationship("Challenge", backref=backref('submission', order_by=id))

    time_created= Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, desc, file, cid, uid):
        if not file:
            raise Exception('The file must be included.')
        self.desc = desc
        self.cid = cid
        self.uid = uid
        self.file = File(self.directory).write(file).name

    def __repr__(self) -> str:
        return ','.join(map(str, [self.desc, self.file, self.cid, self.uid]))
