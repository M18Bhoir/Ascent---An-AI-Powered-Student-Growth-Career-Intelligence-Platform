from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.auth.dependencies import get_current_user
from app.config import settings
from app.database import engine
from app.models.user import User
from app.routers import auth, hod, student


app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Student Growth & Career Intelligence Platform",
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(hod.router)
app.include_router(student.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to Ascent API",
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ascent-backend",
        "version": settings.app_version,
    }


@app.get("/api/v1/health/database")
def database_health_check():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT current_database()")
            )

            database_name = result.scalar()

        return {
            "status": "healthy",
            "database": database_name,
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": None,
            "error": str(error),
        }


@app.get(
    "/api/v1/authenticated",
)
def authenticated_route(
    current_user: User = Depends(
        get_current_user
    ),
):

    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }