from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction_schema import TransactionCreate, TransactionRead
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/transacoes", tags=["Transações"])


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def criar_transacao(
    transacao_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
    usuario: User = Depends(get_current_user)
):
    """Cria uma transação (depósito ou saque) vinculada a uma conta."""
    query = select(Account).where(Account.id == transacao_data.conta_id, Account.usuario_id == usuario.id)
    result = await session.execute(query)
    conta = result.scalars().first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário")

    # Validação de valor
    if transacao_data.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor deve ser positivo")

    # Atualiza saldo de acordo com o tipo de transação
    if transacao_data.tipo.lower() == "deposito":
        conta.saldo += transacao_data.valor
    elif transacao_data.tipo.lower() == "saque":
        if conta.saldo < transacao_data.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente para saque")
        conta.saldo -= transacao_data.valor
    else:
        raise HTTPException(status_code=400, detail="Tipo de transação inválido (use 'deposito' ou 'saque')")

    # Cria e persiste a transação
    nova_transacao = Transaction(
        tipo=transacao_data.tipo.lower(),
        valor=transacao_data.valor,
        conta_id=conta.id
    )

    session.add(nova_transacao)
    await session.commit()
    await session.refresh(nova_transacao)

    return nova_transacao


@router.get("/extrato/{conta_id}", response_model=list[TransactionRead])
async def listar_transacoes(
    conta_id: int,
    session: AsyncSession = Depends(get_session),
    usuario: User = Depends(get_current_user)
):
    """Retorna o extrato (todas as transações) de uma conta."""
    query_conta = select(Account).where(Account.id == conta_id, Account.usuario_id == usuario.id)
    result_conta = await session.execute(query_conta)
    conta = result_conta.scalars().first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário")

    query = select(Transaction).where(Transaction.conta_id == conta.id).order_by(Transaction.criado_em.desc())
    result = await session.execute(query)
    transacoes = result.scalars().all()

    return transacoes
