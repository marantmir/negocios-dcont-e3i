from fastapi import FastAPI
from app.modules.mercado_livre.routes import router as ml_router
from app.modules.erp.routes import router as erp_router
from app.modules.ai_insights.routes import router as ai_router

app = FastAPI(
    title="MeliOps AI",
    description="Integração inteligente entre Mercado Livre, ERP, financeiro, fiscal e contábil.",
    version="1.0.0"
)

app.include_router(ml_router, prefix="/mercado-livre", tags=["Mercado Livre"])
app.include_router(erp_router, prefix="/erp", tags=["ERP"])
app.include_router(ai_router, prefix="/ai", tags=["AI Insights"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MeliOps AI"}
