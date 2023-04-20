from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    user: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    host: str = os.getenv("POSTGRES_HOST")
    port: str = os.getenv("POSTGRES_PORT")
    name: str = os.getenv("POSTGRES_NAME")

    timezone: str = os.getenv("TZ")

    test_user: str = os.getenv("TEST_POSTGRES_USER")
    test_password: str = os.getenv("TEST_POSTGRES_PASSWORD")
    test_host: str = os.getenv("TEST_POSTGRES_HOST")
    test_port: str = os.getenv("TEST_POSTGRES_PORT")
    test_name: str = os.getenv("TEST_POSTGRES_NAME")


settings = Settings()
