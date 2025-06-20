from fastapi import HTTPException, Depends, FastAPI

from auth import UserClaims, validate_access

server = FastAPI()


@server.get("/vulnerable/admin")
def vulnerable_get_admin(user_claims: UserClaims = Depends(validate_access)):
    return "success!"


@server.get("/admin")
def get_admin(user_claims: UserClaims = Depends(validate_access)):
    if "admin" in user_claims.permissions:
        return "success!"
    raise HTTPException(status_code=401, detail="Unauthorized")
