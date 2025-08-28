from datetime import datetime, timezone, timedelta

from jose import jwt

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.apithreats.com",
    "sub": "23456543",
    "aud": "https://apithreats.com/api",
    "iat": now,
    "exp": (now + timedelta(hours=1)),
}


token = jwt.encode(claims=payload, key="password", algorithm="HS256")

print(token)
