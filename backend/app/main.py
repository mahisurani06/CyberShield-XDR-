from fastapi import FastAPI

from app.database.database import engine
from app.models.user import User
from app.database.database import Base
from app.routes.auth import router as auth_router


# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberShield XDR API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "CyberShield XDR Backend Running"
    }