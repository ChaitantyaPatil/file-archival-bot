import shutil
import os
import time
import zipfile
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.config.settings import SOURCE_DIR, TARGET_DIR, ARCHIVE_DIR, DATE_FORMAT
from project.main import process_file, scan_directory

def setup_test_env():
    # consistent testing state
    if SOURCE_DIR.exists(): shutil.rmtree(SOURCE_DIR)
    if TARGET_DIR.exists(): shutil.rmtree(TARGET_DIR)
    if ARCHIVE_DIR.exists(): shutil.rmtree(ARCHIVE_DIR)

    SOURCE_DIR.mkdir(parents=True)
    TARGET_DIR.mkdir(parents=True)
    ARCHIVE_DIR.mkdir(parents=True)

    # Create dummy files
    (SOURCE_DIR / "test_doc.txt").write_text("dummy content")
    (SOURCE_DIR / "test_img.jpg").write_text("dummy image content")
    (SOURCE_DIR / "test_music.mp3").write_text("dummy music content")
    
    # Create a locked file sim (can't easily lock in script without blocking, skipping for simple test)

def verify_results():
    date_str = datetime.now().strftime(DATE_FORMAT)
    
    # check moves
    assert (TARGET_DIR / "documents" / "test_doc.txt").exists(), "Document not moved"
    assert (TARGET_DIR / "images" / "test_img.jpg").exists(), "Image not moved"
    assert (TARGET_DIR / "music" / "test_music.mp3").exists(), "Music not moved"
    
    # check source empty
    assert not (SOURCE_DIR / "test_doc.txt").exists(), "Source doc still exists"
    
    # check archives
    doc_zip = ARCHIVE_DIR / f"documents_{date_str}.zip"
    assert doc_zip.exists(), "Document ZIP not created"
    
    with zipfile.ZipFile(doc_zip, 'r') as zf:
        assert "test_doc.txt" in zf.namelist(), "test_doc.txt not in ZIP"

    print("Integration Test PASSED!")
    
if __name__ == "__main__":
    setup_test_env()
    print("Files created. Running processing...")
    
    # scan and process
    for file_path in list(scan_directory(SOURCE_DIR)):
        process_file(file_path)
        
    verify_results()
