"""Main application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up application...")
    yield
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="{project_name}",
    description="{project_description}",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to {project_name}",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "{project_name}",
    }


@app.get("/ready", response_class=JSONResponse)
async def readiness_check():
    """Readiness check endpoint for orchestrators."""
    # TODO: Add actual readiness checks (DB, cache, etc.)
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
        },
    }


def main():
    """Main entry point for CLI."""
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
