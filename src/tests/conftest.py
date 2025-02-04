import pytest_asyncio
from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from src.db import get_session
from src.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session():
    """
    Override for the get_session dependency that yields sessions from our test engine.
    """
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


def run_migrations(connection):
    config = Config("src/alembic.ini")
    config.set_main_option("script_location", "src/migrations")
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": SQLModel.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    # Run alembic migrations on test DB
    async with test_engine.begin() as connection:
        await connection.run_sync(run_migrations)

    yield

    # Teardown
    await test_engine.dispose()


# @pytest_asyncio.fixture(scope="module", autouse=True)
# async def prepare_database():
#     """
#     Create all tables before tests run and drop them after tests complete.
#     """
#     async with test_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
