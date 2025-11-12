from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.transaction import Transaction
from app.core.database import get_session

router = APIRouter(prefix="/transacoes", tags=["Transações"])

@router.get("/")
async def listar_transacoes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Transaction))
    transacoes = result.scalars().all()
    return {"mensagem": "Listagem de transações bem-sucedida", "dados": transacoes}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_transacao(transacao: Transaction, session: AsyncSession = Depends(get_session)):
    session.add(transacao)
    await session.commit()
    await session.refresh(transacao)
    return {"mensagem": "Transação criada com sucesso", "dados": transacao}

@router.get("/{transacao_id}")
async def buscar_transacao(transacao_id: int, session: AsyncSession = Depends(get_session)):
    transacao = await session.get(Transaction, transacao_id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"mensagem": "Transação encontrada", "dados": transacao}

@router.delete("/{transacao_id}")
async def deletar_transacao(transacao_id: int, session: AsyncSession = Depends(get_session)):
    transacao = await session.get(Transaction, transacao_id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    await session.delete(transacao)
    await session.commit()
    return {"mensagem": "Transação removida com sucesso"}
