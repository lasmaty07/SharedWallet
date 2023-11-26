import re
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine, event, inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from config.settings import settings


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


Base = declarative_base()


class SQLBaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    id = Column(Integer, primary_key=True)
    created_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    deleted_at: datetime = Column(
        DateTime(timezone=True), index=True, nullable=True
    )

    def as_dict(self):
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self).mapper.column_attrs
        }


@event.listens_for(SQLBaseModel, "before_update", propagate=True)
def updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
