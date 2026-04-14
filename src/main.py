from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import auth, authors, books
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.models.user import User
from app.models.book import Book
from app.models.author import Author


Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A secure task manager API with JWT authentication",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
