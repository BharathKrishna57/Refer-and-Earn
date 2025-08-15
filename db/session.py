from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ✅ Dummy local SQLite database
DATABASE_URL = "sqlite:///./dummy.db"  # File-based DB
# If you don't want to persist data at all, use:
# DATABASE_URL = "sqlite:///:memory:"

# Create engine for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite multithreading
)

# Session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Optional: Auto-create all tables on startup
def init_db():
    from your_models_file import *  # Import all SQLAlchemy models here
    Base.metadata.create_all(bind=engine)
