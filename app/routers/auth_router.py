# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.core.database import get_session
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar(dados: dict, session: AsyncSession = Depends(get_session)):
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        raise HTTPException(status_code=400, detail="Nome, e-mail e senha são obrigatórios")

    # Verifica se o e-mail já existe
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    usuario_existente = result.scalars().first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # Criptografa a senha
    senha_hash = get_password_hash(senha)

    usuario = User(nome=nome, email=email, senha_hash=senha_hash)
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)

    return {"mensagem": "Usuário registrado com sucesso", "dados": {"id": usuario.id, "email": usuario.email}}


@router.post("/login")
async def login(dados: dict, session: AsyncSession = Depends(get_session)):
    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        raise HTTPException(status_code=400, detail="E-mail e senha são obrigatórios")

    query = select(User).where(User.email == email)
    result = await session.execute(query)
    usuario = result.scalars().first()

    if not usuario or not verify_password(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(subject=str(usuario.id))
    return {
        "mensagem": "Login realizado com sucesso",
        "access_token": access_token,
        "token_type": "bearer",
    }
