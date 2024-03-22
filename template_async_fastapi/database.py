import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from fastapi import Depends
from template_async_fastapi.models import *  # noqa: F401, F403
from template_async_fastapi.models import BaseModel

# Will fail loudly if environment variable is not there
DB_URL = os.environ["DB_URL"]


class DBSession:
    instance = None


engine: AsyncEngine = create_async_engine(DB_URL, pool_pre_ping=True)
session_factory = async_sessionmaker(engine, class_=AsyncEngine, expire_on_commit=False)

async with engine.begin() as temp_connection:
    temp_connection.run_sync(BaseModel.metadata.create_all)


async def _get_session() -> AsyncEngine:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            await session.close()


class DB(AsyncSession):
    def __new__(cls, db: AsyncSession = Depends(_get_session)) -> AsyncSession:
        return db
