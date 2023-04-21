import datetime

from pydantic import PositiveInt, NonNegativeInt

from serializers.base_schema import (
    ModelSchema,
    CreateModelSchema,
    UpdateModelSchema,
    GetModelsByQuerySchema,
    DeleteModelSchema,
    GetModelSchema,
)


class UserSchema(ModelSchema):
    id: PositiveInt
    username: str
    email: str
    password_hash: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class CreateUserSchema(CreateModelSchema):
    username: str
    email: str
    password_hash: str


class UpdateUserSchema(UpdateModelSchema):
    username: str | None
    email: str | None
    password_hash: str | None


class GetUserSchema(GetModelSchema):
    id: PositiveInt


class GetUsersByQuerySchema(GetModelsByQuerySchema):
    limit: PositiveInt = 1000
    offset: NonNegativeInt = 0


class DeleteUserSchema(DeleteModelSchema):
    id: PositiveInt
