import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Base Paths
SOURCE_DIR = Path(os.getenv("SOURCE_DIR", "./data/incoming"))
TARGET_DIR = Path(os.getenv("TARGET_DIR", "./data/processed"))
ARCHIVE_DIR = Path(os.getenv("ARCHIVE_DIR", "./data/archive"))

# Ensure directories exist
SOURCE_DIR.mkdir(parents=True, exist_ok=True)
TARGET_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Date Format
DATE_FORMAT = os.getenv("DATE_FORMAT", "%d%m%Y")

# Categories
CATEGORIES = {
    "images": os.getenv("EXT_IMAGES", ".jpg,.jpeg,.png,.gif").split(","),
    "music": os.getenv("EXT_MUSIC", ".mp3,.wav").split(","),
    "videos": os.getenv("EXT_VIDEOS", ".mp4,.avi").split(","),
    "documents": os.getenv("EXT_DOCUMENTS", ".pdf,.docx,.xlsx").split(","),
}

# Logging
LOG_FILE = Path(os.getenv("LOG_FILE", "./logs/archival_bot.log"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True) # Ensure log dir exists

# Retry Settings
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))

# Validation
ENABLE_CHECKSUM = os.getenv("ENABLE_CHECKSUM", "True").lower() == "true"
