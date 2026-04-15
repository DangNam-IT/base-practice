from fastapi import FastAPI, Request, Response
from typing import Callable
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import auth, authors, books
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.models.user import User
from app.models.book import Book
from app.models.author import Author
from app.logger import get_logger, setup_logging


logger = get_logger(__name__)
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────
    setup_logging(level="DEBUG")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    logger.info("Bookstore API started successfully")
    yield
    # ── Shutdown ─────────────────────────────────
    logger.info("Bookstore API shutting down")
 


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A secure task manager API with JWT authentication",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Middleware: log mọi request/response ─────────────────
 
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("← %s %s [%d]", request.method, request.url.path, response.status_code)
    return response

# Include all routers
app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    
    **Returns:** Health status of the application
    """
    return {"status": "healthy", "app": settings.APP_NAME}


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict:
    """
    Root endpoint - API information.
    
    **Returns:** Welcome message and API version
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
