import base64
import json
from datetime import datetime, timezone
from typing import Annotated

import requests
from fastapi import HTTPException, Depends, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwcrypto import jwt, jwk
from jwcrypto.jwt import JWTInvalidClaimValue
from pydantic import BaseModel


server = FastAPI()

jwks_endpoint = "https://apithreats.eu.auth0.com/.well-known/jwks.json"

jwks = requests.get(jwks_endpoint).json()["keys"]

security = HTTPBearer()


class UserClaims(BaseModel):
    sub: str


def find_public_key(kid):
    for key in jwks:
        if key["kid"] == kid:
            return key


@server.get("/validate-token-vulnerable")
def validate_token_vulnerable(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        unverified_header = json.loads(
            base64.urlsafe_b64decode(credentials.credentials.split(".")[0])
        )
        key = jwk.JWK(**find_public_key(unverified_header["kid"]))
        encrypted_token = jwt.JWT(
            key=key,
            jwt=credentials.credentials,
            algs=["RS256"],
        )
        return encrypted_token.claims
    except (JWTInvalidClaimValue,) as error:
        raise HTTPException(status_code=401, detail=str(error))


@server.get("/validate-token")
def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        unverified_header = json.loads(
            base64.urlsafe_b64decode(credentials.credentials.split(".")[0])
        )
        key = jwk.JWK(**find_public_key(unverified_header["kid"]))
        encrypted_token = jwt.JWT(
            key=key,
            jwt=credentials.credentials,
            algs=["RS256"],
            check_claims={
                "aud": "https://apithreats.com/admin",
                "exp": datetime.now(timezone.utc).timestamp(),
            },
        )
        return encrypted_token.claims
    except (JWTInvalidClaimValue,) as error:
        raise HTTPException(status_code=401, detail=str(error))
