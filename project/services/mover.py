import shutil
import os
from pathlib import Path
from project.utils.helpers import calculate_checksum, get_unique_filename
from project.utils.logger import setup_logger
from project.config.settings import ENABLE_CHECKSUM

logger = setup_logger("mover")

def move_file(src: Path, dest_folder: Path) -> Path:
    """
    Moves a file to the destination folder safely.
    Returns the path to the moved file.
    """
    if not src.exists():
        raise FileNotFoundError(f"Source file {src} not found.")
    
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_path = get_unique_filename(dest_folder, src.name)

    # Checksum before move
    src_checksum = None
    if ENABLE_CHECKSUM:
        src_checksum = calculate_checksum(src)
        logger.debug(f"Source checksum for {src}: {src_checksum}")

    # Move file
    try:
        shutil.move(str(src), str(dest_path))
    except Exception as e:
        logger.error(f"Failed to move {src} to {dest_path}: {e}")
        raise

    # Validation after move
    if ENABLE_CHECKSUM:
        dest_checksum = calculate_checksum(dest_path)
        logger.debug(f"Dest checksum for {dest_path}: {dest_checksum}")
        
        if src_checksum != dest_checksum:
            logger.critical(f"Checksum mismatch for {src.name}! Verification failed.")
            # Start rollback or alert (In this simple version, we log critical error)
            raise ValueError(f"Integrity check failed for {src.name}")

    logger.info(f"Moved {src} -> {dest_path}")
    return dest_path
