from pathlib import Path
import re

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr

DB_PATH = Path(__file__).resolve().parents[2] / "football.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Declarative base for ORM models.

    Auto-derives `__tablename__` from the class name: CamelCase is converted to
    snake_case and an `s` is appended. Examples:
        Team        -> teams
        Player      -> players
        UserAccount -> user_accounts

    Iirregular English nouns will produce incorrect names
    (e.g. `Person` -> `persons` instead of `people`). 
    For those cases, override `__tablename__` explicitly in the
    subclass.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return f"{snake}s"


async def get_session():
    async with SessionLocal() as session:
        yield session
