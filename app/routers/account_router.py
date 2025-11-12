from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.account import Account
from app.core.database import get_session

router = APIRouter(prefix="/contas", tags=["Contas"])

@router.get("/")
async def listar_contas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account))
    contas = result.scalars().all()
    return {"mensagem": "Listagem de contas bem-sucedida", "dados": contas}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_conta(conta: Account, session: AsyncSession = Depends(get_session)):
    session.add(conta)
    await session.commit()
    await session.refresh(conta)
    return {"mensagem": "Conta criada com sucesso", "dados": conta}

@router.get("/{conta_id}")
async def buscar_conta(conta_id: int, session: AsyncSession = Depends(get_session)):
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"mensagem": "Conta encontrada", "dados": conta}

@router.put("/{conta_id}")
async def atualizar_conta(conta_id: int, dados: Account, session: AsyncSession = Depends(get_session)):
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    conta.numero = dados.numero
    conta.saldo = dados.saldo
    await session.commit()
    await session.refresh(conta)
    return {"mensagem": "Conta atualizada com sucesso", "dados": conta}

@router.delete("/{conta_id}")
async def deletar_conta(conta_id: int, session: AsyncSession = Depends(get_session)):
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    await session.delete(conta)
    await session.commit()
    return {"mensagem": "Conta removida com sucesso"}
