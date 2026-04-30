from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models import FinancialEntry, OrderItem

router = APIRouter()

@router.get("/summary")
def financial_summary(company_id: int = 1, db: Session = Depends(get_db)):
    revenue = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0)).filter(FinancialEntry.company_id == company_id, FinancialEntry.type == "receivable").scalar()
    fees = db.query(func.coalesce(func.sum(OrderItem.sale_fee), 0)).scalar()
    return {"revenue": float(revenue or 0), "marketplace_fees": float(fees or 0), "estimated_net": float((revenue or 0) - (fees or 0))}
