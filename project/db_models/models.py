from project.db_models.base import Base
from sqlalchemy import Column, String, Integer
from project.db_models.mixin import DictMixin

class AccountTransactionTemplate(Base, DictMixin):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)