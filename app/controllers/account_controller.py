# app/controllers/account_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime

from app.models.account import Account
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.account_schema import AccountCreate, AccountRead
from app.schemas.transaction_schema import TransactionCreate, TransactionRead
from app.core.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/contas", tags=["Contas"])


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    conta_data: AccountCreate,
    session: AsyncSession = Depends(get_session),
    usuario: User = Depends(get_current_user)
):
    """Cria uma nova conta bancária vinculada ao usuário autenticado."""
    query = select(Account).where(Account.numero == conta_data.numero)
    result = await session.execute(query)
    conta_existente = result.scalars().first()

    if conta_existente:
        raise HTTPException(status_code=400, detail="Número de conta já existe")

    nova_conta = Account(
        numero=conta_data.numero,
        saldo=conta_data.saldo,
        usuario_id=usuario.id
    )

    session.add(nova_conta)
    await session.commit()
    await session.refresh(nova_conta)

    return nova_conta


@router.post("/{conta_id}/deposito", response_model=TransactionRead)
async def depositar(
    conta_id: int,
    transacao_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
    usuario: User = Depends(get_current_user)
):
    """Realiza um depósito em uma conta do usuário autenticado."""
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if conta.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem acesso a esta conta")

    if transacao_data.tipo.lower() != "deposito":
        raise HTTPException(status_code=400, detail="Tipo inválido para depósito")

    conta.saldo += transacao_data.valor
    transacao = Transaction(
        tipo="deposito",
        valor=transacao_data.valor,
        conta_id=conta.id,
        criado_em=datetime.utcnow()
    )

    session.add(transacao)
    await session.commit()
    await session.refresh(transacao)

    return transacao


@router.post("/{conta_id}/saque", response_model=TransactionRead)
async def sacar(
    conta_id: int,
    transacao_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
    usuario: User = Depends(get_current_user)
):
    """Realiza um saque em uma conta do usuário autenticado."""
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if conta.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem acesso a esta conta")

    if transacao_data.tipo.lower() != "saque":
        raise HTTPException(status_code=400, detail="Tipo inválido para saque")

    if transacao_data.valor > conta.saldo:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para saque")

    conta.saldo -= transacao_data.valor
    transacao = Transaction(
        tipo="saque",
        valor=transacao_data.valor,
        conta_id=conta.id,
        criado_em=datetime.utcnow()
    )

    session.add(transacao)
    await session.commit()
    await session.refresh(transacao)

    return transacao
