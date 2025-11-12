from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# ============================================================
# Configuração principal do banco de dados
# ============================================================

# URL do banco de dados (por enquanto SQLite local)
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Cria o engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Cria a fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# ============================================================
# Função de dependência para obter a sessão
# ============================================================

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fornece uma sessão assíncrona para interação com o banco.
    Usada como dependência nas rotas.
    """
    async with AsyncSessionLocal() as session:
        yield session

# ============================================================
# Inicialização do banco de dados
# ============================================================

async def init_db() -> None:
    """
    Cria as tabelas no banco de dados de forma assíncrona.
    Deve ser chamada no evento de inicialização do FastAPI.
    """
    import app.models.user  # importa modelos para registrar as tabelas
    import app.models.account
    import app.models.transaction

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Banco de dados inicializado com sucesso!")
