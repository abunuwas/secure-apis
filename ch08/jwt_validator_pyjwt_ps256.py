from pathlib import Path

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key

public_key = load_pem_public_key(Path("public_key.pem").read_text().encode())


def validate_token(token):
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=["PS256"],
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
    )


token = "<token>"  # paste your token here
print(validate_token(token))
