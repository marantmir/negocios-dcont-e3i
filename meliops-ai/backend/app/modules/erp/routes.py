from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ERPConnection
from app.core.security import encrypt_value, decrypt_value
from app.modules.erp.client import GenericERPClient

router = APIRouter()

class ERPConnectionRequest(BaseModel):
    company_id: int = 1
    erp_name: str
    base_url: str
    api_key: str

@router.post("/connections")
def create_connection(payload: ERPConnectionRequest, db: Session = Depends(get_db)):
    conn = ERPConnection(company_id=payload.company_id, erp_name=payload.erp_name, base_url=payload.base_url, api_key_enc=encrypt_value(payload.api_key))
    db.add(conn)
    db.commit()
    return {"message": "Conexão ERP criada", "id": conn.id}

@router.post("/connections/{connection_id}/test")
def test_connection(connection_id: int, db: Session = Depends(get_db)):
    conn = db.query(ERPConnection).filter(ERPConnection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Conexão ERP não encontrada")
    client = GenericERPClient(conn.base_url, decrypt_value(conn.api_key_enc))
    return {"message": "Cliente ERP configurado", "erp": conn.erp_name}
