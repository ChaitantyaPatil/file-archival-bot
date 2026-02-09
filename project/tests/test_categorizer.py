import pytest
from pathlib import Path
from project.services.categorizer import get_category

def test_get_category_images():
    assert get_category(Path("test.jpg")) == "images"
    assert get_category(Path("test.PNG")) == "images"

def test_get_category_music():
    assert get_category(Path("song.mp3")) == "music"

def test_get_category_videos():
    assert get_category(Path("movie.mp4")) == "videos"

def test_get_category_documents():
    assert get_category(Path("doc.pdf")) == "documents"
    assert get_category(Path("sheet.xlsx")) == "documents"

def test_get_category_others():
    assert get_category(Path("unknown.xyz")) == "others"
    assert get_category(Path("script.py")) == "others"
