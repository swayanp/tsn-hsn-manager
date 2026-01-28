# app/services/identifier_service.py

from sqlalchemy.orm import Session
from typing import List

from app.models.identifier import Identifier
from sqlalchemy import func, case



def add_identifiers(
    db: Session,
    values: List[str],
    id_type: str,
    product: str,
    source: str
):
    inserted = 0
    skipped = 0

    for value in values:
        existing = db.query(Identifier).filter(
            Identifier.value == value
        ).first()

        if existing:
            skipped += 1
            continue

        identifier = Identifier(
            value=value,
            type=id_type,
            product=product,
            status="AVAILABLE",
            source=source
        )

        db.add(identifier)
        inserted += 1

    db.commit()

    return {
        "inserted": inserted,
        "skipped": skipped
    }
from datetime import datetime


def get_next_identifier(db, id_type: str, product: str):
    identifier = (
        db.query(Identifier)
        .filter(
            Identifier.type == id_type,
            Identifier.product == product,
            Identifier.status == "AVAILABLE"
        )
        .order_by(Identifier.id.asc())
        .first()
    )

    if not identifier:
        return None

    identifier.status = "USED"
    identifier.used_at = datetime.utcnow()
    db.commit()

    return identifier.value
def get_available_count(db, id_type: str, product: str) -> int:
    return (
        db.query(Identifier)
        .filter(
            Identifier.type == id_type,
            Identifier.product == product,
            Identifier.status == "AVAILABLE"
        )
        .count()
    )
from sqlalchemy import func


def get_dashboard_data(db):
    """
    Returns product-wise inventory summary
    """
    results = (
        db.query(
            Identifier.product,
            Identifier.type,
            func.count(Identifier.id).label("total"),
            func.sum(
                case(
                    (Identifier.status == "AVAILABLE", 1),
                    else_=0
                )
            ).label("available"),
            func.sum(
                case(
                    (Identifier.status == "USED", 1),
                    else_=0
                )
            ).label("used"),
        )
        .group_by(Identifier.product, Identifier.type)
        .all()
    )

    dashboard = {}

    for row in results:
        dashboard[row.product] = {
            "type": row.type,
            "total": row.total,
            "available": row.available,
            "used": row.used,
            "low_stock": row.available <= 10
        }

    return dashboard
