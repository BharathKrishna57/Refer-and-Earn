from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
 
from app.config import FRONTEND_URL
from app.db.session import engine
from app.models.vfh_models import Base
from app.api.refer_router import router as refer_router
from app.api.pincode import router as pincode
# Load environment variables from .env file
load_dotenv()
 
# Initialize database tables (only if needed)
Base.metadata.create_all(bind=engine)
 
# Initialize FastAPI app
app = FastAPI(title="Refer-A-Friend API")
 
# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # e.g., "http://localhost:4210"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Register API router
app.include_router(refer_router)
 
app.include_router(pincode, prefix="/api")