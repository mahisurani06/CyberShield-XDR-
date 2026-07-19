from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetResponse
from app.auth.oauth2 import get_current_user
from app.security.roles import analyst_required, admin_required

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("/", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(analyst_required)
):
    existing_asset = db.query(Asset).filter(
        Asset.ip_address == asset.ip_address
    ).first()

    if existing_asset:
        raise HTTPException(
            status_code=400,
            detail="Asset with this IP already exists"
        )

    new_asset = Asset(
        hostname=asset.hostname,
        ip_address=asset.ip_address,
        operating_system=asset.operating_system,
        asset_type=asset.asset_type,
        owner=asset.owner
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/", response_model=list[AssetResponse])
def get_assets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Asset).all()


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    db.delete(asset)
    db.commit()

    return {
        "message": "Asset deleted successfully"
    }