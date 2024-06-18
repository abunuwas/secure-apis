import uuid
from typing import Annotated

import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jws, ExpiredSignatureError, JWTError, JWSError, jwt
from jose.exceptions import JWTClaimsError
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class OrderModel(Base):
    __tablename__ = "order"

    user: Mapped[str]
    product: Mapped[str]
    quantity: Mapped[int]


engine = create_engine("sqlite:///bola.db")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


fixture_orders = [
    {
        "user": str(uuid.uuid4()),
        "product": "Cloak of invisibility",
        "quantity": 1,
    },
    {
        "user": str(uuid.uuid4()),
        "product": "Deluminator",
        "quantity": 1,
    },
]

with session_maker() as session:
    if not list(session.scalars(select(OrderModel))):
        orders = [OrderModel(**order_details) for order_details in fixture_orders]
        session.add_all(orders)
        session.commit()


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


@server.get("/vulnerable/orders/{order_id}")
def vulnerable_get_order_details(order_id: int):
    with session_maker() as session:
        order = session.scalar(select(OrderModel).where(OrderModel.id == order_id))
        if order is None:
            raise HTTPException(
                status_code=404, detail=f"Order with ID {order_id} not found."
            )
    return {
        "id": order.id,
        "product": order.product,
        "quantity": order.quantity,
    }


@server.get("/orders/{order_id}")
def get_order_details(order_id: int, user_claims: UserClaims = Depends(validate_token)):
    with session_maker() as session:
        order = session.scalar(
            select(OrderModel).where(
                OrderModel.id == order_id, OrderModel.user == user_claims.sub
            )
        )
        if order is None:
            raise HTTPException(
                status_code=404, detail=f"Order with ID {order_id} not found."
            )
    return {
        "id": order.id,
        "product": order.product,
        "quantity": order.quantity,
    }
