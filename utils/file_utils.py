ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime_type(filename: str) -> str | None:
    ext = filename.rsplit(".", 1)[1].lower()
    if ext == "png":
        return "image/png"
    if ext in {"jpg", "jpeg"}:
        return "image/jpeg"
    return None