from sqlalchemy import String, Column

from infrastructure.persistance.base import SQLBaseModel


class User(SQLBaseModel):
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
