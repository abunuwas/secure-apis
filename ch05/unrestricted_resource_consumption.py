from collections import defaultdict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests import Request
from starlette.responses import JSONResponse

server = FastAPI()


users_db = [{"email": "sarah.connor@apithreats.com", "password": "asdf"}]


login_attempts_ips = defaultdict(int)
login_attempts_accounts = defaultdict(int)

blocked_ips = []
locked_accounts = []


@server.middleware("http.request")
async def prevent_brute_force_login(request: Request, call_next):
    if request.client.host in blocked_ips:
        return JSONResponse(status_code=401, content={"error": "Blocked"})

    if request.url.path != "/login":
        return await call_next(request)

    body = await request.body()
    if not body:
        return await call_next(request)

    payload = await request.json()

    if payload["email"] in locked_accounts:
        return JSONResponse(status_code=401, content={"error": "Locked"})

    login_attempts_ips[request.client.host] += 1
    login_attempts_accounts[payload["email"]] += 1

    if login_attempts_ips[request.client.host] == 10:
        blocked_ips.append(request.client.host)

    if login_attempts_accounts[payload["email"]] == 10:
        locked_accounts.append(payload["email"])
        login_attempts_accounts[payload["email"]] = 0

    return await call_next(request)


class LoginSchema(BaseModel):
    email: str
    password: str


class LoginSuccessSchema(BaseModel):
    message: str


@server.post("/login", response_model=LoginSuccessSchema)
def login(login_details: LoginSchema):
    for user in users_db:
        if (
            user["email"] == login_details.email
            and user["password"] == login_details.password
        ):
            return {"message": "success!"}
    raise HTTPException(status_code=401, detail={"error": "Wrong email or password"})
