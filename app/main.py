from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import user_router, account_router, transaction_router, auth_router, banking_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Servidor inicializado com sucesso!")
    yield
    print("Servidor finalizado!")


app = FastAPI(
    title="API Bancária Async",
    version="1.0.0",
    description="API bancária assíncrono. @andrepimentelsantos01",
    lifespan=lifespan,
)

# Inclui as rotas de usuários
app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(transaction_router.router)
app.include_router(auth_router.router)
app.include_router(banking_router.router)