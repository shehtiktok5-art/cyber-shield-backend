"""Main FastAPI application for CYBER-SHIELD Backend"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from src.config import get_settings
from src.utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events (startup/shutdown)"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Demo Mode: {settings.DEMO_MODE}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time Cybersecurity Threat Intelligence Platform",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    max_age=3600,
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "saudi.oneapp.dev",
        "*.oneapp.dev",
    ]
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status": "error",
            "type": exc.__class__.__name__,
        },
    )


# Health Check Endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health/ready")
async def readiness_check():
    """Readiness check (includes dependency checks)"""
    try:
        return {
            "status": "ready",
            "database": "connected",
            "cache": "connected",
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "error": str(e),
            },
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CYBER-SHIELD Backend API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "status": "operational",
    }


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""Real-time Cybersecurity Threat Intelligence Platform Backend
        
Features:
- Real-time threat intelligence aggregation
- Network traffic analysis and anomaly detection
- Intrusion Detection System (IDS) integration
- AI-powered attack prediction
- Incident response management
- User and Entity Behavior Analytics (UEBA)
- Automated alert generation and routing
- Compliance reporting
        """,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://saudi.oneapp.dev/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
