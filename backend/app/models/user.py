from app import db
from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__("uuid").uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hash and store password."""
        self.password_hash = hashpw(password.encode(), gensalt(10)).decode()

    def check_password(self, password):
        """Verify password against hash."""
        return checkpw(password.encode(), self.password_hash.encode())

    def to_dict(self):
        """Return usr data as dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
        }