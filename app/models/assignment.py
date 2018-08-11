from app import db

from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignment'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = db.Column(db.Integer, primary_key=True, unique=True)
    title       = db.Column(db.String(64))
    content     = db.Column(db.Text)
    cate        = db.Column(db.Integer)
    start       = db.Column(db.DateTime)
    due         = db.Column(db.DateTime)
    created     = db.Column(db.DateTime)
    submissions = db.relationship("submission")

    def __init__(self, id, title, content, cate, start, due):
        self.id = id
        self.title = title
        self.content = content
        self.cate = cate
        self.start = start
        self.due = due
        self.created = datetime.now()

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.content, self.cate, self.start, self.due]))

    def __dict__(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
