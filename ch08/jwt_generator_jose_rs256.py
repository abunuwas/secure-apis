from datetime import datetime, timezone, timedelta
from pathlib import Path

from jose import jwt

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.apithreats.com",
    "sub": "23456543",
    "aud": "https://apithreats.com/api",
    "iat": now,
    "exp": (now + timedelta(hours=1)),
}

signing_key = Path("private_key.pem").read_text()

token = jwt.encode(claims=payload, key=signing_key, algorithm="RS256")

print(token)
