import argparse
import sys
import time
from pathlib import Path
from project.config.settings import SOURCE_DIR, TARGET_DIR, ARCHIVE_DIR, RETRY_COUNT, RETRY_DELAY
from project.utils.logger import setup_logger
from project.services.file_scanner import scan_directory, is_file_stable, is_file_locked
from project.services.categorizer import get_category
from project.services.mover import move_file
from project.services.zipper import archive_file

logger = setup_logger()

def process_file(file_path: Path, dry_run: bool = False):
    """
    Processes a single file: categorize -> move -> archive.
    """
    try:
        # 1. Stability Checks
        if not is_file_stable(file_path):
            logger.warning(f"File {file_path.name} is unstable (size changing). Skipping.")
            return

        if is_file_locked(file_path):
            logger.warning(f"File {file_path.name} is locked by another process. Skipping.")
            return

        # 2. Categorize
        category = get_category(file_path)
        logger.info(f"Categorized {file_path.name} as {category}")

        # 3. Determine Paths
        target_folder = TARGET_DIR / category
        
        if dry_run:
            logger.info(f"[DRY-RUN] Would move {file_path} -> {target_folder}")
            logger.info(f"[DRY-RUN] Would archive to {category} ZIP")
            return

        # 4. Move File (with Retry)
        moved_path = None
        for attempt in range(1, RETRY_COUNT + 1):
            try:
                moved_path = move_file(file_path, target_folder)
                break
            except Exception as e:
                logger.error(f"Attempt {attempt}/{RETRY_COUNT} failed to move {file_path}: {e}")
                if attempt < RETRY_COUNT:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Failed to move {file_path} after {RETRY_COUNT} attempts.")
                    return # Skip archiving if move failed

        # 5. Archive File (Sequential - could be async)
        # We archive the MOVED file, not the source (which is gone)
        if moved_path:
            try:
                archive_file(moved_path, category)
            except Exception as e:
                logger.error(f"Failed to archive {moved_path}: {e}")
                # Note: File is already moved, so we don't rollback the move, just log the archive failure.

    except Exception as e:
        logger.exception(f"Unexpected error processing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Python File Archival & Categorization System")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files")
    parser.add_argument("--once", action="store_true", help="Run once and exit (default behavior for now)")
    # Future: --loop or --schedule
    
    args = parser.parse_args()

    logger.info("Starting File Archival System...")
    logger.info(f"Source: {SOURCE_DIR}")
    logger.info(f"Target: {TARGET_DIR}")
    logger.info(f"Archive: {ARCHIVE_DIR}")

    if args.dry_run:
        logger.info("RUNNING IN DRY-RUN MODE")

    # Single pass scanning
    files = list(scan_directory(SOURCE_DIR))
    logger.info(f"Found {len(files)} files to process.")

    for file_path in files:
        process_file(file_path, dry_run=args.dry_run)

    logger.info("Processing completed.")

if __name__ == "__main__":
    main()
