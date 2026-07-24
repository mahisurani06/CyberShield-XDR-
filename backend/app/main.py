

from fastapi import FastAPI
from app.models.asset import Asset 
from app.models.alert import Alert
from app.database.database import engine
from app.models.user import User
from app.models.incident import Incident
from app.database.database import Base
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.admin import router as admin_router
from app.routes.assets import router as assets_router
from app.routes.incidents import router as incidents_router
from app.routes.alerts import router as alerts_router
from app.routes.dashboard import router as dashboard_router
from app.models.audit_log import AuditLog 
from app.routes.audit_log import router as audit_router
from app.routes.threat_intel import router as threat_router


# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberShield XDR API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(assets_router)
app.include_router(incidents_router) 
app.include_router(alerts_router)
app.include_router(dashboard_router)
app.include_router(audit_router) 
app.include_router(threat_router)

@app.get("/")
def root():
    return {
        "message": "CyberShield XDR Backend Running"
    }