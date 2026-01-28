# app/models/identifier.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.database import Base


class Identifier(Base):
    __tablename__ = "identifiers"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)      # TSN or HSN
    product = Column(String, nullable=False)   # EDGE_CABLE, etc
    status = Column(String, nullable=False)    # AVAILABLE, USED
    source = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
