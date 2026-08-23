from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.router import api_router
from app.lifespan import lifespan
from core.logger import logger
from core.config import ALLOW_ORIGINS

from core.config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan,
)

# ==========================================================
# CORS Middleware
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Register API Routes
# ==========================================================

app.include_router(api_router)

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(
    "/",
    tags=["Root"],
    summary="Welcome API",
)
async def root():
    logger.info("Root API called.")

    return {
        "success": True,
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": f"Welcome to {APP_NAME}",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
)
async def health_check():
    return {
        "success": True,
        "status": "Healthy",
    }
