from contextlib import asynccontextmanager
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

from threading import local
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

metadata = MetaData()
thread_local = local()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base(metadata=metadata)


@asynccontextmanager
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()


async def get_db_dependency():
    async with get_db() as db:
        yield db
