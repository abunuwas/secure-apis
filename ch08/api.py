import os
from typing import Annotated

import jwt
import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from starlette.responses import RedirectResponse

client_id = os.getenv("AUTH0_CLIENT_ID")
client_secret = os.getenv("AUTH0_CLIENT_SECRET")
jwks_endpoint = os.getenv("JWKS_ENDPOINT")

assert client_id is not None, "AUTH0_CLIENT_ID environment variable needed"
assert client_secret is not None, "AUTH0_CLIENT_SECRET environment variable needed"
assert jwks_endpoint is not None, "JWKS_ENDPOINT env variable needed"

jwks = requests.get(jwks_endpoint).json()["keys"]

server = FastAPI()

jwks_client = jwt.PyJWKClient(jwks_endpoint)


def validate_token(token, audience):
    return jwt.decode(
        jwt=token,
        key=jwks_client.get_signing_key_from_jwt(token),
        algorithms=["RS256"],
        audience=audience,
        issuer="<issuer>",  # e.g.: https://apithreats.eu.auth0.com/
    )


security = HTTPBearer()


def authorize_access(creds: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        return validate_token(creds.credentials, audience="https://apithreats.com")
    except PyJWTError as error:
        raise HTTPException(status_code=401, detail=str(error))


@server.get("/protected-hello")
def protected_hello(user_claims: dict = Depends(authorize_access)):
    return {"message": f"hello {user_claims['sub']}"}


@server.get("/hello")
def hello():
    return {"message": "hello"}


@server.get("/login")
def register():
    return RedirectResponse(
        "<authorization_endpoint>"  # e.g.: https://apithreats.eu.auth0.com/authorize
        "?response_type=code"
        f"&client_id={client_id}"
        "&redirect_uri=http://localhost:8000/docs"
        "&audience=<audience>"  # e.g.: https://apithreats.com
    )


@server.get("/token")
def get_access_token(code: str):
    payload = (
        "grant_type=authorization_code"
        f"&client_id={client_id}"
        f"&client_secret={client_secret}"
        f"&code={code}"
        "&redirect_uri=http://localhost:8000/docs"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "<token_endpoint>",  # e.g.: https://apithreats.eu.auth0.com/oauth/token
        payload,
        headers=headers,
    )
    return response.json()


admin_client_id = os.getenv("AUTH0_ADMIN_CLIENT_ID")
admin_client_secret = os.getenv("AUTH0_ADMIN_CLIENT_SECRET")

assert admin_client_id is not None, "AUTH0_ADMIN_CLIENT_ID env variable needed"
assert admin_client_secret is not None, "AUTH0_ADMIN_CLIENT_SECRET env variable needed"


def authorize_admin_access(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        claims = validate_token(
            creds.credentials,
            audience="<audience>",  # e.g.: https://apithreats.com/admin
        )
    except PyJWTError as error:
        raise HTTPException(status_code=401, detail=str(error))
    if "admin" not in claims.get("permissions", []):
        raise HTTPException(
            status_code=401, detail="Sorry, this endpoint is only for admins"
        )
    return claims


@server.get("/admin/login")
def admin_login():
    return RedirectResponse(
        "<authorization_endpoint>"  # e.g.: https://apithreats.eu.auth0.com/authorize
        "?response_type=code"
        f"&client_id={admin_client_id}"
        "&redirect_uri=http://localhost:8000/docs"
        "&audience=<audience>"  # e.g.: https://apithreats.com/admin
    )


@server.get("/admin/hello")
def admin_hello(user_claims: dict = Depends(authorize_admin_access)):
    return {"message": f"hello admin {user_claims['sub']}"}


@server.get("/token")
def get_admin_access_token(code: str):
    payload = (
        "grant_type=authorization_code"
        f"&client_id={admin_client_id}"
        f"&client_secret={admin_client_secret}"
        f"&code={code}"
        "&redirect_uri=http://localhost:8000/docs"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "<token_endpoint>",  # e.g.: https://apithreats.eu.auth0.com/oauth/token
        payload,
        headers=headers,
    )
    return response.json()
