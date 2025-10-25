from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.features.client import router as client_router
from app.features.query import router as query_router
from app.shared.config import settings

app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
    description=f"{settings.API_NAME} - {settings.API_VERSION}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(query_router)


@app.get("/")
async def root():
    return {
        "name": settings.API_NAME,
        "version": settings.API_VERSION,
        "status": "running",
    }


@app.get("/healthcheck")
async def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc)
            if settings.DEBUG
            else "An unexpected error occurred",
        },
    )
