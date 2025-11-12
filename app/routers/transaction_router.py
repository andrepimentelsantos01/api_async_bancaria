from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/transacoes", tags=["Transações"])

transacoes = []

@router.get("/")
async def listar_transacoes():
    return {"mensagem": "Listagem de transações bem-sucedida", "dados": transacoes}

@router.post("/")
async def criar_transacao(transacao: dict):
    transacoes.append(transacao)
    return {"mensagem": "Transação criada com sucesso", "dados": transacao}

@router.get("/{transacao_id}")
async def buscar_transacao(transacao_id: int):
    if transacao_id >= len(transacoes) or transacao_id < 0:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"mensagem": "Transação encontrada", "dados": transacoes[transacao_id]}

@router.put("/{transacao_id}")
async def atualizar_transacao(transacao_id: int, transacao: dict):
    if transacao_id >= len(transacoes) or transacao_id < 0:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    transacoes[transacao_id] = transacao
    return {"mensagem": "Transação atualizada com sucesso", "dados": transacao}

@router.delete("/{transacao_id}")
async def deletar_transacao(transacao_id: int):
    if transacao_id >= len(transacoes) or transacao_id < 0:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    transacoes.pop(transacao_id)
    return {"mensagem": "Transação removida com sucesso"}
