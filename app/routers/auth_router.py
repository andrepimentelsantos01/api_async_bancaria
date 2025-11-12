from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/auth", tags=["Autenticação"])

usuarios = [{"email": "teste@banco.com", "senha": "1234"}]

@router.post("/login")
async def login(dados: dict):
    email = dados.get("email")
    senha = dados.get("senha")

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            return {"mensagem": "Login realizado com sucesso", "token": "token_simulado_123"}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/logout")
async def logout():
    return {"mensagem": "Logout realizado com sucesso"}

@router.post("/registrar")
async def registrar(dados: dict):
    usuarios.append(dados)
    return {"mensagem": "Usuário registrado com sucesso", "dados": dados}
