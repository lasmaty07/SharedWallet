from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.exceptions import EntityAlreadyExists
from infrastructure.persistance.models.group import Group
from api.v1.schemas.group_schemas import (
    GroupCreate,
    GroupRead,
)


class GroupRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def to_domain(group: Group) -> GroupRead:
        return GroupRead(
            id=group.id,
            created_at=group.created_at,
            updated_at=group.updated_at,
            deleted_at=group.deleted_at,
            name=group.name,
            description=group.description,
        )

    @staticmethod
    def to_persistance(group: GroupCreate) -> Group:
        return Group(name=group.name, description=group.description)

    def add(self, group: Group) -> GroupRead:
        self.session.add(group)
        try:
            self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExists

        self.session.refresh(group)
        return group

    def get_all(self, page_size: int, page: int):
        groups = self.session.execute(
            select(Group)
            .where(Group.deleted_at == None)
            .limit(page_size)
            .offset(page_size * page)
        ).all()
        return [group[0] for group in groups]

    def get_without_map(self, group_id: int) -> Group:
        group = self.session.execute(
            select(Group).where(
                Group.id == group_id,
                Group.deleted_at == None,
            )
        ).first()
        if group:
            return group[0]

    def get(self, group_id: int) -> GroupRead | None:
        group = self.session.execute(
            select(Group).where(
                Group.id == group_id,
                Group.deleted_at == None,
            )
        ).first()
        if group:
            return self.to_domain(group[0])

    def update(self, group: Group) -> GroupRead:
        self.session.commit()
        self.session.refresh(group)
        return self.to_domain(group)

    def delete(self, group_id: int):
        group = self.session.execute(
            select(Group).where(Group.id == group_id)
        ).first()
        if group:
            group[0].deleted_at = datetime.now()
            self.session.commit()
            return True
        return False
