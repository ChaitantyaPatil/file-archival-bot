import hashlib
from pathlib import Path
import time
from typing import Optional

def calculate_checksum(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Calculates the checksum of a file.
    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        # Read in chunks to avoid memory issues with large files
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_unique_filename(directory: Path, filename: str) -> Path:
    """
    Returns a unique filename in the directory by appending a timestamp if needed.
    """
    file_path = directory / filename
    if not file_path.exists():
        return file_path
    
    stem = file_path.stem
    suffix = file_path.suffix
    timestamp = int(time.time())
    new_filename = f"{stem}_{timestamp}{suffix}"
    return directory / new_filename
