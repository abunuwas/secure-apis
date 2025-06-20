from datetime import datetime, timedelta

import jwt

now = datetime.utcnow()

payload = {
    "iss": "https://auth.apithreats.com",
    "sub": "23456543",
    "aud": "https://apithreats.com/api",
    "iat": now,
    "exp": (now + timedelta(hours=1)).timestamp(),
}

print(jwt.encode(payload=payload, key="password", algorithm="HS256"))
