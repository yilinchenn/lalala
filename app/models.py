from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    photos = db.relationship('Photo', backref=db.backref('user', lazy=True))


    def __init__(self, username, password, is_admin):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s Pswd_hash %s Admin %s>' % (self.username, self.password_hash, self.is_admin)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Integer)
    path = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, photo_id, type, path):
        self.photo_id = photo_id
        self.type = type
        self.path = path

    def __repr__(self):
        return '<id %s Photo_id %s type %s user_id %s>' % (self.id, self.photo_id, self.type, self.user_id)