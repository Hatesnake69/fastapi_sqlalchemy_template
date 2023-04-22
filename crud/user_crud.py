from sqlalchemy import and_, update, delete
from sqlalchemy.future import select

from crud.base_crud import BaseCRUD
from models import UserModel
from serializers import (
    UserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    GetUserSchema,
    GetUsersByQuerySchema,
    DeleteUserSchema,
)


class UserCRUD(BaseCRUD):
    model = UserModel

    async def create_user(self, cmd: CreateUserSchema) -> UserSchema:
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
        return UserSchema.from_orm(new_instance)

    async def get_user(self, cmd: GetUserSchema) -> UserSchema:
        model_instance = await self.session.get(entity=self.model, ident=cmd.id)
        return UserSchema.from_orm(model_instance)

    async def filter(self, cmd: GetUsersByQuerySchema) -> list[UserSchema]:
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
        res = [
            UserSchema.from_orm(instance_elem)
            for instance_elem in rows.scalars().fetchall()
        ]
        return res

    async def update_user(self, cmd: UpdateUserSchema) -> UserSchema:
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
        res = (
            await self.session.execute(
                update(self.model)
                .where(self.model.id == cmd.id)
                .values(dict_of_values)
                .returning(self.model)
            )
        ).scalar()
        await self.session.commit()
        print(res)
        return UserSchema.from_orm(res)

    async def delete_user(self, cmd: DeleteUserSchema) -> UserSchema:
        res = (
            await self.session.execute(
                delete(self.model).where(self.model.id == cmd.id).returning(self.model)
            )
        ).scalar()
        await self.session.commit()
        return UserSchema.from_orm(res)
