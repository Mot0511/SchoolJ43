from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv, find_dotenv
import os

from db.models import Base

load_dotenv(find_dotenv())

engine = create_async_engine(os.getenv('DB'))
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=True, class_=AsyncSession)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with sessionmaker() as session:
        yield session