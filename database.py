# database.py
import os
import time
from databases import Database # type: ignore
from sqlalchemy import create_engine, MetaData # type: ignore
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost/url_shortener")
print("DATABASE_URL =", DATABASE_URL)
# Convert old-style URL if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


database = Database(DATABASE_URL)
metadata = MetaData()

# engine = create_engine(DATABASE_URL)
engine = None
while engine is None:
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("Database is ready!")
    except OperationalError:
        print("Database not ready yet. Waiting...")
        time.sleep(2)