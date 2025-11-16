from fastapi import FastAPI

from core.routes import router as org_router

app = FastAPI(
    title="MKK LUNA",
    description="REST SERVICE",
    version="1.0.0"
)
app.include_router(org_router)
