from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError, JWSError
from pydantic import BaseModel


class UserClaims(BaseModel):
    sub: str
    role: str


def authorize_access(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    try:
        claims = jwt.decode(
            token=credentials.credentials,
            key="secret",
            audience="https://apithreats.com",
            algorithms="HS256",
        )
    except (
        ExpiredSignatureError,
        JWTError,
        JWTClaimsError,
        JWSError,
    ) as error:
        raise HTTPException(status_code=401, detail=str(error))
    return UserClaims(sub=claims["sub"], role=claims["role"])


def create_access_token(sub: str, is_admin: bool = False):
    if is_admin:
        return jwt.encode(claims={"sub": sub, "role": "admin"}, key="secret")
    return jwt.encode(claims={"sub": sub, "role": "student"}, key="secret")
