from api import db
from api.models.author import AuthorModel


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)
    rate = db.Column(db.Integer)

    def __init__(self, author: AuthorModel, text: str, rate=0):
        self.author_id = author.id
        self.text = text
        self.rate = rate

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author.to_dict(),
            "rate": self.rate
        }

