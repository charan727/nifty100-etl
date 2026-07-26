from fastapi import FastAPI
from src.api.routers import screener
from src.api.routers import dashboard
from src.api.routers import documents
from src.api.routers import portfolio
from src.api.routers import peer
from src.api.routers import tearsheet
from src.api.routers import reports
from src.api.routers import health
from src.api.routers import companies
from src.api.routers import ratios
from src.api.routers import valuation
from src.api.routers import sectors
app = FastAPI(
    title="NIFTY100 API",
    version="1.0.0"
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
    tags=["Sectors"]
)
app.include_router(
    screener.router,
    prefix="/api/v1",
    tags=["Screener"]
)
app.include_router(
    peer.router,
    prefix="/api/v1",
    tags=["Peer Groups"]
)
app.include_router(
    dashboard.router,
    prefix="/api/v1",
    tags=["Dashboard"]
)
app.include_router(
    portfolio.router,
    prefix="/api/v1",
    tags=["Portfolio"]
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(ratios.router, prefix="/api/v1", tags=["Ratios"])
app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])
app.include_router(documents.router)
app.include_router(tearsheet.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "message": "NIFTY100 API Running"
    }