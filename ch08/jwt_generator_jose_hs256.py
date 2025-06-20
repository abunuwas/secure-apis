from datetime import datetime, timezone, timedelta

from jose import jwt

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.apithreats.com",
    "sub": "10",
    "aud": "https://pyconus2024.com",
    "iat": now.timestamp(),
    "exp": (now + timedelta(hours=1)).timestamp(),
}


token = jwt.encode(claims=payload, key="password", algorithm="HS256")

print(token)
