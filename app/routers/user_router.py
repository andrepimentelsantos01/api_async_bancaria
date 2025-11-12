from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

usuarios = []

@router.get("/")
async def listar_usuarios():
    return {"mensagem": "Listagem de usuários bem-sucedida", "dados": usuarios}

@router.post("/")
async def criar_usuario(usuario: dict):
    usuarios.append(usuario)
    return {"mensagem": "Usuário criado com sucesso", "dados": usuario}

@router.get("/{usuario_id}")
async def buscar_usuario(usuario_id: int):
    if usuario_id >= len(usuarios) or usuario_id < 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário encontrado", "dados": usuarios[usuario_id]}

@router.put("/{usuario_id}")
async def atualizar_usuario(usuario_id: int, usuario: dict):
    if usuario_id >= len(usuarios) or usuario_id < 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuarios[usuario_id] = usuario
    return {"mensagem": "Usuário atualizado com sucesso", "dados": usuario}

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: int):
    if usuario_id >= len(usuarios) or usuario_id < 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuarios.pop(usuario_id)
    return {"mensagem": "Usuário removido com sucesso"}
