from pathlib import Path
from project.config.settings import CATEGORIES

def get_category(file_path: Path) -> str:
    """
    Determines the category of a file based on its suffix.
    Returns 'others' if no category matches.
    """
    suffix = file_path.suffix.lower()
    
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
            
    return "others"
