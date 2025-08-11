from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  # ✅ Add this line
 
DATABASE_URL = "mysql+pymysql://root:Bharath%4057@localhost/my_database"
 
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
 
# ✅ Add this line to expose `Base` for model files
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





