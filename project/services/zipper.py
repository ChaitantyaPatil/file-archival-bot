import zipfile
import os
from datetime import datetime
from pathlib import Path
from project.config.settings import DATE_FORMAT, ARCHIVE_DIR
from project.utils.logger import setup_logger

logger = setup_logger("zipper")

def archive_file(file_path: Path, category: str):
    """
    Adds a file to the daily ZIP archive for the given category.
    Naming: <category>_DDMMYYYY.zip
    """
    if not file_path.exists():
        logger.error(f"File to archive not found: {file_path}")
        return

    date_str = datetime.now().strftime(DATE_FORMAT)
    zip_filename = f"{category}_{date_str}.zip"
    zip_path = ARCHIVE_DIR / zip_filename

    try:
        # 'a' mode appends to existing zip or creates new one
        with zipfile.ZipFile(zip_path, 'a', zipfile.ZIP_DEFLATED) as zf:
            # Arcname is the name inside the zip. We just want the filename, not full path.
            zf.write(file_path, arcname=file_path.name)
            
        logger.info(f"Archived {file_path.name} to {zip_path}")
    except Exception as e:
        logger.error(f"Failed to archive {file_path}: {e}")
        raise
