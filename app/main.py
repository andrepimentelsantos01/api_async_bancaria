from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.controllers.auth_controller import router as auth_router
from app.controllers.account_controller import router as account_router
from app.controllers.transaction_controller import router as transaction_router
from app.controllers.root_controller import router as root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Inicializando banco de dados...")
    await init_db()
    print("✅ Banco de dados pronto!")
    yield
    print("🛑 Encerrando aplicação...")


app = FastAPI(
    title="API Bancária Assíncrona",
    description="API RESTful para gerenciamento de contas, transações e autenticação JWT.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)
