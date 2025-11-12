from fastapi import FastAPI
from app.routers import user_router, account_router, transaction_router, auth_router, banking_router
from app.core.database import init_db

# ============================================================
# Inicialização da aplicação
# ============================================================

app = FastAPI(title="API Bancária Assíncrona", version="1.0.0")

# ============================================================
# Registro das rotas
# ============================================================

app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(transaction_router.router)
app.include_router(auth_router.router)
app.include_router(banking_router.router)

# ============================================================
# Ciclo de vida do app (startup e shutdown)
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    await init_db()
    print("🚀 Servidor e banco inicializados com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento ao finalizar o servidor"""
    print("🛑 Servidor finalizado!")
