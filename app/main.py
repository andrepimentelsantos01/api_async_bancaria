from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from app.routers import (
    user_router,
    account_router,
    transaction_router,
    auth_router,
    banking_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("🚀 Servidor e banco inicializados com sucesso!")
    yield
    print("🛑 Servidor finalizado!")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(transaction_router.router)
app.include_router(auth_router.router)
app.include_router(banking_router.router)
