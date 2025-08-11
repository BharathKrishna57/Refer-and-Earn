from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Use the remote freesqldatabase.com connection string
DATABASE_URL = "mysql+pymysql://sql12794254:AB8FAY5dPj@sql12.freesqldatabase.com:3306/sql12794254"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
