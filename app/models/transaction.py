from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.account import Account

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    valor: float
    tipo: str
    data: datetime = Field(default_factory=datetime.utcnow)

    conta_id: int = Field(foreign_key="account.id")
    conta: "Account" = Relationship(back_populates="transacoes")
