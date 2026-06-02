from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


# echo=True on the engine during development.
# It prints every SQL query SQLAlchemy generates to the terminal.
# Invaluable for debugging async queries.
engine = create_async_engine(settings.DATABASE_URL, echo=True)


LocalSession = async_sessionmaker(engine)


async def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        await session.close()
