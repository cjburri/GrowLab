import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug mode configuration
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() in ('true', '1', 't') 