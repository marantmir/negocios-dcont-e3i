from fastapi import APIRouter, Request, HTTPException
import requests
from app.core.config import settings
from app.modules.mercado_livre.client import MercadoLivreClient

router = APIRouter()

@router.get("/auth-url")
def get_auth_url():
    url = (
        "https://auth.mercadolivre.com.br/authorization"
        f"?response_type=code"
        f"&client_id={settings.MELI_CLIENT_ID}"
        f"&redirect_uri={settings.MELI_REDIRECT_URI}"
    )
    return {"auth_url": url}

@router.get("/callback")
def mercado_livre_callback(code: str):
    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.MELI_CLIENT_ID,
        "client_secret": settings.MELI_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.MELI_REDIRECT_URI
    }

    response = requests.post(
        "https://api.mercadolibre.com/oauth/token",
        data=payload,
        timeout=30
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=response.text)

    token_data = response.json()

    return {
        "message": "Conta Mercado Livre conectada com sucesso.",
        "seller_id": token_data.get("user_id"),
        "expires_in": token_data.get("expires_in")
    }

@router.post("/webhook")
async def mercado_livre_webhook(request: Request):
    payload = await request.json()

    # Aqui você grava o evento recebido numa fila/tabela para processamento assíncrono
    # Exemplo de payload: orders, payments, shipments, items etc.

    return {"received": True, "payload": payload}
