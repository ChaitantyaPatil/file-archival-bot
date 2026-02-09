import os
import time
from pathlib import Path
from typing import List, Generator
from project.utils.logger import setup_logger

logger = setup_logger("file_scanner")

def scan_directory(directory: Path) -> Generator[Path, None, None]:
    """
    Yields files from the directory, skipping directories.
    """
    if not directory.exists():
        logger.error(f"Source directory {directory} does not exist.")
        return

    for entry in directory.iterdir():
        if entry.is_file():
            yield entry

def is_file_stable(file_path: Path, wait_time: int = 1) -> bool:
    """
    Checks if a file is stable (upload finished) by comparing size over an interval.
    """
    try:
        size_initial = file_path.stat().st_size
        time.sleep(wait_time)
        size_final = file_path.stat().st_size
        return size_initial == size_final
    except OSError as e:
        logger.warning(f"Error checking stability for {file_path}: {e}")
        return False

def is_file_locked(file_path: Path) -> bool:
    """
    Checks if a file is locked by another process.
    """
    try:
        # Try to rename the file to itself. This is an atomic check for write access/lock on Windows.
        # Alternatively, opening in specific modes can work, but rename is a strong check.
        # However, rename to self might be optimized out or behave differently.
        # Let's try opening with exclusive write access.
        with open(file_path, 'a+'):
            pass
        return False
    except IOError:
        return True
