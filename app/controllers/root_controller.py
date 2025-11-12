from fastapi import APIRouter

router = APIRouter(tags=["Root"])


@router.get("/", include_in_schema=False)
async def root():
    return {
        "mensagem": "API Bancária Assíncrona",
        "status": "online",
        "nota": "Use /docs para ver a documentação OpenAPI"
    }
