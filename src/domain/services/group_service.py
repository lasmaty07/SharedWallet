from typing import List
from sqlalchemy.orm import Session

from api.v1.schemas.group_schemas import (
    GroupRead,
    GroupCreate,
    GroupUpdate,
)
from domain.exceptions import EntityNotExists
from infrastructure.persistance.models.group import Group
from infrastructure.persistance.repositories.group_repository import (
    GroupRepository,
)


class GroupService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = GroupRepository(self.session)

    def get_groups(self, page_size: int, page: int) -> List[GroupCreate]:
        return [
            self.repository.to_domain(group)
            for group in self.repository.get_all(page_size, page)
        ]

    def get_group(self, group_id: int) -> GroupRead:
        instance: Group = self.repository.get(group_id)
        if not instance:
            raise EntityNotExists
        group_read = self.repository.to_domain(instance)
        return group_read

    def create_group(
        self,
        group_create: GroupCreate,
    ) -> GroupRead:
        group = self.repository.to_persistance(group_create)
        group_read = self.repository.add(group)
        return group_read

    def update_group(
        self,
        group_id: int,
        group_update: GroupUpdate,
    ) -> GroupRead:
        group: Group = self.repository.get_without_map(group_id)
        if not group:
            raise EntityNotExists
        for k, v in group_update.dict(exclude_unset=True).items():
            if v:
                setattr(group, k, v)
        group_read = self.repository.update(group)
        return group_read

    def delete_group(self, group_id: int):
        return self.repository.delete(group_id)
