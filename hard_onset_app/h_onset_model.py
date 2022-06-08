from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    baseline = db.Column(db.Integer)


def init_db():
    db.create_all()
    new_user = User('test', 'test@example.com', 0)
    db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    init_db()
