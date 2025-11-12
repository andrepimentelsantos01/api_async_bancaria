from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/contas", tags=["Contas"])

contas = []

@router.get("/")
async def listar_contas():
    return {"mensagem": "Listagem de contas bem-sucedida", "dados": contas}

@router.post("/")
async def criar_conta(conta: dict):
    contas.append(conta)
    return {"mensagem": "Conta criada com sucesso", "dados": conta}

@router.get("/{conta_id}")
async def buscar_conta(conta_id: int):
    if conta_id >= len(contas) or conta_id < 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"mensagem": "Conta encontrada", "dados": contas[conta_id]}

@router.put("/{conta_id}")
async def atualizar_conta(conta_id: int, conta: dict):
    if conta_id >= len(contas) or conta_id < 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    contas[conta_id] = conta
    return {"mensagem": "Conta atualizada com sucesso", "dados": conta}

@router.delete("/{conta_id}")
async def deletar_conta(conta_id: int):
    if conta_id >= len(contas) or conta_id < 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    contas.pop(conta_id)
    return {"mensagem": "Conta removida com sucesso"}
