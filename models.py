import sqlalchemy
import datetime

metadata = sqlalchemy.MetaData()

links = sqlalchemy.Table(
    "links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("original_url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("short_url", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), default=datetime.datetime.utcnow),  # Use timezone=True
    sqlalchemy.Column("expiration_date", sqlalchemy.DateTime(timezone=True), nullable=True),  # NEW with timezone support
    sqlalchemy.Column("clicks", sqlalchemy.Integer, default=0),  # For Step 2
)
