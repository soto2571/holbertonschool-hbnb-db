"""
User model for the application
"""

from typing import Any
from src import db
from src.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


class User(Base):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # New attribute for admin status
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str,
            is_admin: bool = False,
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,  # Include is_admin in the dictionary representation
        }

    @staticmethod
    def create(data: dict) -> Any:
        # Check if a user with the same email already exists
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=data.get("password"),
            # Handle is_admin in user creation
            is_admin=data.get("is_admin", False)
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError("Database error occurred while creating user.")
        return user

    @staticmethod
    def update(entity_id: str, data: dict) -> Any:
        user = User.query.get(entity_id)
        if user is None:
            return None
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        if "password" in data:
            user.password_hash = generate_password_hash(data["password"])
        if "is_admin" in data:
            user.is_admin = data["is_admin"]
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError("Database error occurred while updating user.")
        return user

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError("Database error occurred while deleting user.")
