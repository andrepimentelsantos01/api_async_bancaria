from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from app.models.transaction import Transaction
from app.core.database import get_session

router = APIRouter(prefix="/banco", tags=["Operações Bancárias"])

@router.post("/deposito/{conta_id}")
async def deposito(conta_id: int, valor: float, session: AsyncSession = Depends(get_session)):
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    conta.saldo += valor
    transacao = Transaction(valor=valor, tipo="depósito", conta_id=conta.id)
    session.add(transacao)
    await session.commit()
    await session.refresh(conta)
    return {"mensagem": "Depósito realizado com sucesso", "saldo": conta.saldo}

@router.post("/saque/{conta_id}")
async def saque(conta_id: int, valor: float, session: AsyncSession = Depends(get_session)):
    conta = await session.get(Account, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if conta.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    conta.saldo -= valor
    transacao = Transaction(valor=valor, tipo="saque", conta_id=conta.id)
    session.add(transacao)
    await session.commit()
    await session.refresh(conta)
    return {"mensagem": "Saque realizado com sucesso", "saldo": conta.saldo}

@router.post("/transferencia/")
async def transferencia(origem_id: int, destino_id: int, valor: float, session: AsyncSession = Depends(get_session)):
    conta_origem = await session.get(Account, origem_id)
    conta_destino = await session.get(Account, destino_id)
    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta de origem ou destino não encontrada")
    if conta_origem.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para transferência")
    conta_origem.saldo -= valor
    conta_destino.saldo += valor
    trans_origem = Transaction(valor=valor, tipo="transferência - saída", conta_id=conta_origem.id)
    trans_destino = Transaction(valor=valor, tipo="transferência - entrada", conta_id=conta_destino.id)
    session.add_all([trans_origem, trans_destino])
    await session.commit()
    return {"mensagem": "Transferência realizada com sucesso"}
