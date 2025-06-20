from datetime import datetime, timezone, timedelta
from pathlib import Path

from jwcrypto import jwk, jwt

signing_key = Path("private_key.pem").read_text()

jwk_key = jwk.JWK()
jwk_key.import_from_pem(data=signing_key.encode())

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.pyjobs.works",
    "sub": "23456543",
    "aud": "https://pyjobs.works/jobs",
    "iat": now.timestamp(),
    "exp": (now + timedelta(hours=1)).timestamp(),
}

header = {"alg": "RS256"}

token = jwt.JWT(header=header, claims=payload)
token.make_signed_token(jwk_key)

print(token.serialize())
