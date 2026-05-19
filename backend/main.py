from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import tesouro

app = FastAPI(title="Central finance", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return { "status": "Ok", "message": "Welcome to Central finance API" }

app.include_router(tesouro.router)