from typing import Annotated

import requests
from fastapi import HTTPException, Depends, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jws, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWSError, JWTError
from pydantic import BaseModel

server = FastAPI()

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


def validate_token(
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


@server.get("/vulnerable-admin")
def vulnerable_admin(user_claims: UserClaims = Depends(validate_token)):
    return "success!"


@server.get("/admin")
def get_admin(user_claims: UserClaims = Depends(validate_token)):
    if "admin" in user_claims.permissions:
        return "success!"
    raise HTTPException(status_code=401, detail="Unauthorized")
