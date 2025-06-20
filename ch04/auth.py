from typing import Annotated

import requests
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt, jws
from jose.exceptions import JWTClaimsError, JWSError
from pydantic import BaseModel

jwks_endpoint = "https://apithreats.eu.auth0.com/.well-known/jwks.json"

jwks = requests.get(jwks_endpoint).json()["keys"]

security = HTTPBearer()


class UserClaims(BaseModel):
    sub: str
    permissions: list[str]


def find_public_key(kid):
    for key in jwks:
        if key["kid"] == kid:
            return key


def validate_access(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        unverified_headers = jws.get_unverified_header(credentials.credentials)
        token_payload = jwt.decode(
            token=credentials.credentials,
            key=find_public_key(unverified_headers["kid"]),
            audience="https://apithreats.com",
            algorithms="RS256",
        )
        return UserClaims(
            sub=token_payload["sub"], permissions=token_payload.get("permissions", [])
        )
    except (
        ExpiredSignatureError,
        JWTError,
        JWTClaimsError,
        JWSError,
    ) as error:
        raise HTTPException(status_code=401, detail=str(error))
