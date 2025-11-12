from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.core.database import get_session

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/")
async def listar_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    usuarios = result.scalars().all()
    return {"mensagem": "Listagem de usuários bem-sucedida", "dados": usuarios}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: User, session: AsyncSession = Depends(get_session)):
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return {"mensagem": "Usuário criado com sucesso", "dados": usuario}

@router.get("/{usuario_id}")
async def buscar_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(User, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário encontrado", "dados": usuario}

@router.put("/{usuario_id}")
async def atualizar_usuario(usuario_id: int, dados: User, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(User, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.nome = dados.nome
    usuario.email = dados.email
    usuario.senha_hash = dados.senha_hash
    await session.commit()
    await session.refresh(usuario)
    return {"mensagem": "Usuário atualizado com sucesso", "dados": usuario}

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(User, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await session.delete(usuario)
    await session.commit()
    return {"mensagem": "Usuário removido com sucesso"}