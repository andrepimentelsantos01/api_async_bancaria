from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.core.database import get_session
import hashlib

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
async def login(dados: dict, session: AsyncSession = Depends(get_session)):
    email = dados.get("email")
    senha = dados.get("senha")
    if not email or not senha:
        raise HTTPException(status_code=400, detail="E-mail e senha são obrigatórios")
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    query = select(User).where(User.email == email, User.senha_hash == senha_hash)
    result = await session.execute(query)
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"mensagem": "Login realizado com sucesso", "dados": {"usuario": usuario.email}}

@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar(dados: dict, session: AsyncSession = Depends(get_session)):
    if not dados.get("email") or not dados.get("senha"):
        raise HTTPException(status_code=400, detail="E-mail e senha são obrigatórios")
    senha_hash = hashlib.sha256(dados["senha"].encode()).hexdigest()
    usuario = User(nome=dados["nome"], email=dados["email"], senha_hash=senha_hash)
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return {"mensagem": "Usuário registrado com sucesso", "dados": usuario}
