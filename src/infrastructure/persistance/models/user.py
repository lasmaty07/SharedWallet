from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from infrastructure.persistance.base import SQLBaseModel
from .group import user_group_association


class User(SQLBaseModel):
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    expenses = relationship("Expense", back_populates="user")
    groups = relationship(
        "Group", secondary=user_group_association, back_populates="users"
    )
