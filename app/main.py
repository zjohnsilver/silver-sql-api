from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.shared.config import settings
from app.features.clients import router as clients_router
from app.features.queries import router as queries_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="SQL query execution API for Silver SQL Console"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include feature routers
app.include_router(clients_router)
app.include_router(queries_router)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )

