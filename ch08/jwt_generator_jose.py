from datetime import datetime, timezone, timedelta
from pathlib import Path

from jose import jwt

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.pyjobs.works",
    "sub": "10",
    "aud": "https://pyjobs.works/jobs",
    "iat": now.timestamp(),
    "exp": (now + timedelta(hours=1)).timestamp(),
}

signing_key = Path("private_key.pem").read_text()

token = jwt.encode(claims=payload, key=signing_key, algorithm="RS256")

print(token)
