from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# URL de conexão assíncrona com SQLite
DATABASE_URL = "sqlite+aiosqlite:///./db_banco.db"

# Cria o engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Session local assíncrona
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Função que cria as tabelas
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
