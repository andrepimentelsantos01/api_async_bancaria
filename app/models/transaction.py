# app/models/transaction.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.account import Account

class Transaction(SQLModel, table=True):
    __tablename__ = "transacoes"

    id: Optional[int] = Field(default=None, primary_key=True)
    valor: float = Field(nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    conta_id: int = Field(foreign_key="contas.id", nullable=False)
    conta: "Account" = Relationship(back_populates="transacoes")
