from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models import Order, OrderItem

router = APIRouter()

@router.get("/dashboard")
def sales_dashboard(company_id: int = 1, db: Session = Depends(get_db)):
    total_orders = db.query(func.count(Order.id)).filter(Order.company_id == company_id).scalar()
    total_sales = db.query(func.coalesce(func.sum(Order.paid_amount), 0)).filter(Order.company_id == company_id).scalar()
    top_items = db.query(OrderItem.title, func.sum(OrderItem.quantity).label("qty")).join(Order).filter(Order.company_id == company_id).group_by(OrderItem.title).order_by(func.sum(OrderItem.quantity).desc()).limit(10).all()
    return {"total_orders": total_orders, "total_sales": float(total_sales or 0), "top_items": [{"title": t, "quantity": int(q)} for t, q in top_items]}
