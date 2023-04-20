from abc import ABC
from typing import List, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, update, delete
from sqlalchemy.future import select

from db.session import get_db_session
from models import Base
from serializers.base_schema import (
    ModelSchema,
    CreateModelSchema,
    UpdateModelSchema,
    GetModelSchema,
    GetModelsByQuerySchema,
    DeleteModelSchema,
)

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(ABC):
    model: ModelType = Base

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_model(self, cmd: CreateModelSchema) -> ModelSchema:
        attrs = [attr for attr in dir(self.model) if not attr.startswith("_")]
        dict_of_values = {
            attr: getattr(cmd, attr)
            for attr in attrs
            if attr not in {"id", "metadata", "registry"}
            and getattr(cmd, attr, None) is not None
        }
        new_instance = self.model(**dict_of_values)
        self.session.add(new_instance)
        await self.session.commit()
        return ModelSchema.from_orm(new_instance)

    async def get_model(self, cmd: GetModelSchema) -> ModelSchema:
        model_instance = await self.session.get(entity=self.model, ident=cmd.id)
        return ModelSchema.from_orm(model_instance)

    async def filter(self, cmd: GetModelsByQuerySchema) -> List[ModelSchema]:
        where_filter = []
        attrs = [
            attr
            for attr in dir(self.model)
            if not attr.startswith("_")
            and getattr(cmd, attr, None) is not None
            and attr not in {"limit", "offset", "id", "metadata", "registry"}
        ]
        for attr in attrs:
            where_filter.append(getattr(self.model, attr) == getattr(cmd, attr))

        rows = await self.session.execute(
            select(self.model)
            .where(and_(True, *where_filter))
            .offset(cmd.offset)
            .limit(cmd.limit)
        )
        res = [ModelSchema.from_orm(model) for model in rows.scalars().fetchall()]
        return res

    async def update_model(self, cmd: UpdateModelSchema) -> ModelSchema:
        attrs = [
            attr
            for attr in dir(self.model)
            if not attr.startswith("_")
            and getattr(cmd, attr, None) is not None
            and attr not in {"id", "metadata", "registry"}
        ]
        dict_of_values = {
            getattr(self.model, attr): getattr(cmd, attr) for attr in attrs
        }
        res = await self.session.execute(
            update(self.model)
            .where(self.model.id == cmd.id)
            .values(dict_of_values)
            .returning(self.model)
        )
        await self.session.commit()
        return ModelSchema.from_orm(res.fetchone())

    async def delete_model(self, cmd: DeleteModelSchema) -> ModelSchema:
        res = (
            await self.session.execute(
                delete(self.model).where(self.model.id == cmd.id).returning(self.model)
            )
        ).fetchone()

        await self.session.commit()
        return ModelSchema.from_orm(res)
