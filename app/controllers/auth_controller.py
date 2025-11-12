from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.core.security import get_password_hash, verify_password, create_access_token, get_user_by_email
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registro", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(dados: UserCreate, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == dados.email)
    result = await session.execute(query)
    existente = result.scalars().first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    senha_hash = get_password_hash(dados.senha)
    usuario = User(nome=dados.nome, email=dados.email, senha_hash=senha_hash)
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario


@router.post("/login")
async def login(dados: dict, session: AsyncSession = Depends(get_session)):
    email = dados.get("email")
    senha = dados.get("senha")
    if not email or not senha:
        raise HTTPException(status_code=400, detail="E-mail e senha são obrigatórios")

    usuario = await get_user_by_email(session, email)
    if not usuario or not verify_password(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(subject=str(usuario.id))
    return {"mensagem": "Login realizado com sucesso", "access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def perfil(usuario: User = Depends(lambda: None)):
    raise HTTPException(status_code=501, detail="Endpoint de perfil não implementado aqui")
