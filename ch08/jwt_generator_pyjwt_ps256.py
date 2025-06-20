from datetime import datetime, timezone, timedelta
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.apithreats.com",
    "sub": "23456543",
    "aud": "https://apithreats.com/api",
    "iat": now,
    "exp": (now + timedelta(hours=1)).timestamp(),
}

private_key_text = Path("private_key.pem").read_text()

private_key = serialization.load_pem_private_key(
    data=private_key_text.encode(), password=None
)

print(jwt.encode(payload=payload, key=private_key, algorithm="PS256"))
