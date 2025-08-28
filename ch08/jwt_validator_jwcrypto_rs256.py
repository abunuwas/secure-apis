from datetime import datetime, timezone
from pathlib import Path

from jwcrypto import jwk, jwt

public_certificate = Path("public_key.pem").read_text()
jwk_key = jwk.JWK()
jwk_key.import_from_pem(data=public_certificate.encode())


def validate_token(token):
    encrypted_token = jwt.JWT(
        key=jwk_key,
        jwt=token,
        algs=["RS256"],
        check_claims={
            "aud": "https://apithreats.com/api",
            "iss": "https://auth.apithreats.com",
            "exp": datetime.now(timezone.utc).timestamp(),
        },
    )
    return encrypted_token.claims


token = "<token>"  # paste your token here
print(validate_token(token))
