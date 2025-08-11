import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables with fallbacks
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://refer-earn-praveeen.netlify.app")
DATABASE_URL = os.getenv("DATABASE_URL", "")
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-default-secret-key")

# DEBUG should be a proper boolean
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
