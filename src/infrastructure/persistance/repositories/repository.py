from abc import ABC
from typing import Any

from sqlalchemy.exc import IntegrityError

from domain.exceptions import EntityAlreadyExists


class IRepository(ABC):
    def to_domain(ojb: dict[str, Any] = {}) -> Any:
        raise NotImplementedError

    def to_persistance(obj: dict[str, Any] = {}) -> Any:
        raise NotImplementedError

    def add(self, database_object) -> Any:
        self.session.add(database_object)
        try:
            self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExists

        self.session.refresh(database_object)
        return database_object
