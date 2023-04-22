from tests.test_utils.faker import fake


from crud.user_crud import UserCRUD
from db.session import SessionLocal
from serializers.user_schema import UserSchema, CreateUserSchema


async def create_user(
    username: str = None, email: str = None, password_hash: str = None
) -> UserSchema:
    async with SessionLocal() as session:
        async with session.begin():
            users_crud = UserCRUD(session=session)
            return await users_crud.create_user(
                CreateUserSchema(
                    username=username or fake.name(),
                    email=email or fake.email(),
                    password_hash=password_hash or fake.md5(),
                )
            )
