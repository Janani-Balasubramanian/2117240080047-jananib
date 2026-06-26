import os
import zipfile
import shutil
from pathlib import Path

UPLOAD_FOLDER = "uploads"
EXTRACT_FOLDER = "extracted_projects"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)


def _is_safe_zip_member(member_name: str) -> bool:
    normalized = os.path.normpath(member_name)
    return not normalized.startswith("..") and not normalized == ".." and not os.path.isabs(normalized)


def save_zip(upload_file):
    """
    Save uploaded ZIP file.
    """

    zip_path = os.path.join(UPLOAD_FOLDER, upload_file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return zip_path


def extract_zip(zip_path):
    """
    Extract ZIP safely.
    """

    project_name = Path(zip_path).stem

    extract_path = os.path.join(EXTRACT_FOLDER, project_name)

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(extract_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            if member.is_dir():
                continue
            if not _is_safe_zip_member(member.filename):
                raise ValueError(f"Unsafe ZIP entry: {member.filename}")
        zip_ref.extractall(extract_path)

    return extract_path