# # app/core/database.py

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# from app.core.config import DATABASE_PATH

# # SQLite database URL
# DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# # Create database engine
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# # Session for DB operations
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# # Base class for all DB models
# Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "identifiers.db")

# ✅ Ensure parent directory exists (CRITICAL for containers & CI)
db_path = Path(DATABASE_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False}
)

Base = declarative_base()
