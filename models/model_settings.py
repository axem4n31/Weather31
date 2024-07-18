"""
Setting up PostgreSQL and Redis database engines.
"""
from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

POSTGRE_URL = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:" \
              f"{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:5432/{getenv('POSTGRES_DB')}"
SYNC_POSTGRE_URL = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:" \
                   f"{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:5432/{getenv('POSTGRES_DB')}"

engine = create_async_engine(POSTGRE_URL, echo=True, future=True)
sync_engine = create_engine(SYNC_POSTGRE_URL, echo=True, future=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_session = async_sessionmaker(engine, expire_on_commit=False)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_db():
    db = sync_session()
    try:
        yield db
    finally:
        db.close()


# Dependency
class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


db_helper = DatabaseHelper(
    url=POSTGRE_URL,
    echo=True,
)
