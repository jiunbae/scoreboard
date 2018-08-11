from app import db

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id          = db.Column(db.Integer, primary_key=True, unique=True)
    studentid   = db.Column(db.String(12))
    pw          = db.Column(db.String(32))
    submissions = db.relationship("submission")

    def __init__(self, studentid, pw):
        self.id = id
        self.studentid = studentid
        self.pw = pw

    def __repr__(self) -> str:
        return ','.join(map(str, [self.id, self.title, self.content, self.cate, self.start, self.due]))

    def __dict__(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
