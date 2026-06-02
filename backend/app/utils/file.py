import os


def ensure_file_exists(path: str) -> bool:
    return os.path.exists(path)


def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1].lower()


def safe_filename(filename: str) -> str:
    return filename.replace(" ", "_").lower()