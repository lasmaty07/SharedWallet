from sqlalchemy import ForeignKey, Integer, String, Column, Table
from sqlalchemy.orm import relationship

from infrastructure.persistance.base import SQLBaseModel

user_group_association = Table(
    "user_group_association",
    SQLBaseModel.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)


class Group(SQLBaseModel):
    name = Column(String, index=True)
    description = Column(String)
    users = relationship(
        "User", secondary=user_group_association, back_populates="groups"
    )
    expenses = relationship("Expense", back_populates="group")
