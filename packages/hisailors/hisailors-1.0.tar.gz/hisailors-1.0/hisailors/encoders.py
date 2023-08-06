from urllib.parse import quote


def url_encode(form: dict) -> str:
    return "&".join([f"{k}={quote(str(v))}" for k, v in form.items()])
