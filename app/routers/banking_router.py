from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/banco", tags=["Operações Bancárias"])

saldos = {"conta1": 1000.0, "conta2": 500.0}

@router.get("/saldo/{conta_id}")
async def consultar_saldo(conta_id: str):
    if conta_id not in saldos:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"mensagem": "Saldo consultado com sucesso", "saldo": saldos[conta_id]}

@router.post("/depositar")
async def depositar(dados: dict):
    conta = dados.get("conta_id")
    valor = dados.get("valor")

    if conta not in saldos:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    saldos[conta] += valor
    return {"mensagem": f"Depósito de R$ {valor:.2f} realizado com sucesso", "saldo_atual": saldos[conta]}

@router.post("/sacar")
async def sacar(dados: dict):
    conta = dados.get("conta_id")
    valor = dados.get("valor")

    if conta not in saldos:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if saldos[conta] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    saldos[conta] -= valor
    return {"mensagem": f"Saque de R$ {valor:.2f} realizado com sucesso", "saldo_atual": saldos[conta]}

@router.post("/transferir")
async def transferir(dados: dict):
    origem = dados.get("conta_origem")
    destino = dados.get("conta_destino")
    valor = dados.get("valor")

    if origem not in saldos or destino not in saldos:
        raise HTTPException(status_code=404, detail="Conta de origem ou destino não encontrada")

    if saldos[origem] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    saldos[origem] -= valor
    saldos[destino] += valor

    return {"mensagem": f"Transferência de R$ {valor:.2f} realizada com sucesso", "saldo_origem": saldos[origem], "saldo_destino": saldos[destino]}
