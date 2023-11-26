from sqlalchemy import String, Column

from infrastructure.persistance.base import SQLBaseModel


class Category(SQLBaseModel):
    name = Column(String, nullable=False)
    icon = Column(String)
