from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship


from infrastructure.persistance.base import SQLBaseModel


class Expense(SQLBaseModel):
    name = Column(String, nullable=False)
    expense_type = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="expenses")
    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship("Group", back_populates="expenses")
