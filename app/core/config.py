# app/core/config.py
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "identifiers.db")
LOW_STOCK_THRESHOLD = 10

ALLOWED_TYPES = {"TSN", "HSN"}
ALLOWED_PRODUCTS = {
    "EDGE_CABLE",
    "EDGE_ANTENNA",
    "MINI_LUX",
    "STREAM_4K"
}
