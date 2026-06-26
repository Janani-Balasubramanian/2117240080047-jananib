import os

def get_all_files(project_path):
    """
    Returns all files in the extracted project.
    """

    file_list = []

    for root, dirs, files in os.walk(project_path):

        # Ignore unwanted folders
        dirs[:] = [d for d in dirs if d not in [
            "__pycache__",
            ".git",
            "venv",
            "node_modules",
            ".venv",
            "dist",
            "build"
        ]]

        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)

    return file_list


def read_file_content(file_path, max_size=100000):
    """
    Safely read file content, limiting to text files and max size.
    Returns None if file is binary or too large.
    """
    # Skip binary and non-code files
    skip_extensions = {'.pyc', '.pyo', '.class', '.jar', '.exe', '.dll', '.so', '.o', 
                       '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.tar', '.gz'}
    
    if any(file_path.lower().endswith(ext) for ext in skip_extensions):
        return None
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            return None
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        return content if content.strip() else None
    
    except Exception:
        return None
