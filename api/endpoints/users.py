from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.params import Body

from crud.user_crud import UserCRUD
from serializers import (
    UserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    GetUserSchema,
    GetUsersByQuerySchema,
    DeleteUserSchema,
)


router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.get("/", response_model=List[UserSchema])
async def get_users_by_filter(
    cmd: GetUsersByQuerySchema = Depends(),
    users_crud: UserCRUD = Depends(),
) -> List[UserSchema]:
    return await users_crud.filter(cmd=cmd)


@router.get("/{id:int}", response_model=UserSchema)
async def get_user(
    cmd: GetUserSchema = Depends(),
    users_crud: UserCRUD = Depends(),
) -> UserSchema:
    return await users_crud.get_user(cmd=cmd)


@router.post("/", response_model=UserSchema)
async def create_user(
    cmd: CreateUserSchema = Body(),
    users_crud: UserCRUD = Depends(),
) -> UserSchema:
    return await users_crud.create_user(cmd=cmd)


@router.patch(
    "/{id:int}",
    response_model=UserSchema,
)
async def update_user(
    id: int,
    cmd: UpdateUserSchema = Body(
        ...,
    ),
    users_crud: UserCRUD = Depends(),
) -> UserSchema:
    cmd.id = id
    return await users_crud.update_user(cmd=cmd)


@router.delete("/{id:int}", response_model=UserSchema)
async def delete_user(
    cmd: DeleteUserSchema = Depends(),
    users_crud: UserCRUD = Depends(),
) -> UserSchema:
    return await users_crud.delete_user(cmd=cmd)
