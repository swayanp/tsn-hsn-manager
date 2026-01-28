# app/api/v1/identifiers.py

import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.utils.csv_parser import read_values
from app.services.identifier_service import (
    add_identifiers,
    get_next_identifier,
    get_available_count,
    get_dashboard_data
)
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.config import ALLOWED_PRODUCTS, ALLOWED_TYPES
from app.utils.csv_parser import read_values



# Router must be defined BEFORE using it
router = APIRouter(
    prefix="/api/v1/identifiers",
    tags=["Identifiers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_identifiers(
    file: UploadFile = File(...),
    id_type: str = "TSN",
    product: str = "EDGE_CABLE",
    db: Session = Depends(get_db)
):
    # Validate inputs
    if id_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid id_type. Allowed: {ALLOWED_TYPES}"
        )

    if product not in ALLOWED_PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Allowed: {ALLOWED_PRODUCTS}"
        )

    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=400,
            detail="Only .csv or .xlsx files are supported"
        )

    # Save file temporarily
    import tempfile, shutil

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        values = read_values(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = add_identifiers(
        db=db,
        values=values,
        id_type=id_type,
        product=product,
        source=file.filename
    )

    return {
        "message": "Upload processed successfully",
        "result": result
    }


@router.get("/next")
def get_next_identifier_api(
    id_type: str,
    product: str,
    db: Session = Depends(get_db)
):
    if id_type not in ALLOWED_TYPES or product not in ALLOWED_PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail="Invalid product or identifier type"
        )

    value = get_next_identifier(db, id_type, product)

    if not value:
        raise HTTPException(
            status_code=404,
            detail=f"No available {id_type}s left for {product}"
        )

    remaining = get_available_count(db, id_type, product)

    response = {
        "value": value,
        "remaining": remaining
    }

    if remaining <= 10:
        response["warning"] = (
            f"⚠️ Only {remaining} {id_type}s left for {product}. "
            "Please upload new identifiers."
        )

    return response

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data(db)
