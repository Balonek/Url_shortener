import re, secrets, string

BASE62 = string.digits + string.ascii_letters
_url_re = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

def is_valid_url(url: str) -> bool:
    return bool(_url_re.match(url.strip()))

def generate_slug(k: int = 6) -> str:
    return "".join(secrets.choice(BASE62) for _ in range(k))
