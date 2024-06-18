from app import db

class Ulasan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ulasan = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255))
    predicted_label = db.Column(db.String(255))

    def __rep__(self):
        return '<Ulasan {}>'.format(self.name)