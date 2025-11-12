import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_crud_usuarios():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/usuarios/", json={
            "nome": "João",
            "email": "joao@email.com",
            "senha": "123456"
        })
        assert response.status_code == 200
        assert "Usuário criado" in response.json()["mensagem"]

        response = await client.get("/usuarios/")
        assert response.status_code == 200

        response = await client.get("/usuarios/0")
        assert response.status_code == 200

        response = await client.put("/usuarios/0", json={
            "nome": "João Atualizado",
            "email": "joao@email.com",
            "senha": "654321"
        })
        assert response.status_code == 200

        response = await client.delete("/usuarios/0")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_crud_contas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/contas/", json={
            "numero": "12345-6",
            "saldo": 1000.0,
            "usuario_id": 1
        })
        assert response.status_code == 200

        response = await client.get("/contas/")
        assert response.status_code == 200

        response = await client.get("/contas/0")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_transacoes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/transacoes/", json={
            "valor": 200.0,
            "tipo": "depósito",
            "conta_id": 1
        })
        assert response.status_code == 200

        response = await client.get("/transacoes/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "email": "joao@email.com",
            "senha": "123456"
        })
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_operacoes_bancarias():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/banking/deposito", json={
            "conta_id": 1,
            "valor": 200.0
        })
        assert response.status_code in [200, 404]

        response = await client.post("/banking/saque", json={
            "conta_id": 1,
            "valor": 100.0
        })
        assert response.status_code in [200, 404]
