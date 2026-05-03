from sqlalchemy import Column, String, Boolean, DateTime
from project.db_models.base import Base
from project.db_models.mixin import DictMixin

class UserDBModel(Base, DictMixin):
    __tablename__ = 'users'

    id = Column(String, primary_key=True) # text
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"