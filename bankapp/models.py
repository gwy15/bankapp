# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def create(self, username: str, password: str):
        hashed: str
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
