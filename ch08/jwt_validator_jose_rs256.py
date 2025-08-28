from pathlib import Path

from jose import jwt

public_certificate = Path("public_key.pem").read_text()


def validate_token(token):
    return jwt.decode(
        token,
        key=public_certificate,
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
        algorithms="RS256",
    )


token = "<token>"  # paste your token here
print(validate_token(token))
