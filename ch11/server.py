import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, JWSError, jwt
from jose.exceptions import JWTClaimsError
from opentelemetry import trace
from opentelemetry.metrics import get_meter
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

server = fastapi.FastAPI()
tracer = trace.get_tracer("threat_detection.tracer")


class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float


class ListBooks(BaseModel):
    books: list[Book]


class BookQuantity(BaseModel):
    book_id: int
    quantity: int


class CreateCart(BaseModel):
    books: list[BookQuantity]


class GetCart(CreateCart):
    id: int
    created: datetime


class PlaceOrder(BaseModel):
    cart: int
    credit_card: str


class GetOrder(BaseModel):
    id: int
    books: list[BookQuantity]
    created: datetime


meter = get_meter("orders_meter")
list_books_counter = meter.create_counter("list_books")


@server.get("/books", response_model=ListBooks)
async def list_books():
    list_books_counter.add(1)
    return {
        "books": [
            {
                "id": 1,
                "title": "Microservice APIs",
                "author": "Jose Haro Peralta",
                "price": 40,
            },
            {
                "id": 2,
                "title": "Hacking APIs",
                "author": "Corey Ball",
                "price": 40,
            },
            {
                "id": 3,
                "title": "Black Hat GraphQL",
                "author": "Dolev Fahi and Nick Aleks",
                "price": 40,
            },
        ]
    }


carts = []
orders = []


class UserClaims(BaseModel):
    sub: str


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
    return UserClaims(sub=claims["sub"])


class Credentials(BaseModel):
    username: str
    password: str


@server.post("/login")
def login(credentials: Credentials):
    return {
        "access_token": jwt.encode(claims={"sub": credentials.username}, key="secret")
    }


@server.post("/carts", response_model=GetCart, status_code=status.HTTP_201_CREATED)
async def create_cart(
    request: Request,
    cart_details: CreateCart,
    user_claims: UserClaims = Depends(authorize_access),
):
    cart = cart_details.dict()
    with tracer.start_as_current_span("cart.create") as span:
        span.set_attribute("user.sub", user_claims.sub)
        span.set_attribute("request.headers", json.dumps(dict(request.headers)))
        span.set_attribute("http.request_body", cart_details.model_dump_json())
    cart["id"] = len(carts) + 1
    cart["created"] = datetime.now(timezone.utc)
    carts.append(cart)
    return cart


meter = get_meter("orders_meter")
place_order_counter = meter.create_counter("place_order")


@server.post("/orders", response_model=GetOrder, status_code=status.HTTP_201_CREATED)
async def place_order(
    request: Request,
    order_details: PlaceOrder,
    user_claims: UserClaims = Depends(authorize_access),
):
    place_order_counter.add(
        1, {"sub": user_claims.sub, "headers": json.dumps(dict(request.headers))}
    )
    with tracer.start_as_current_span("cart.create") as span:
        span.set_attribute("user.sub", user_claims.sub)
        span.set_attribute("request.headers", json.dumps(dict(request.headers)))
        span.set_attribute(
            "http.request_body", order_details.model_dump_json(exclude=["credit_card"])
        )
    order = order_details.dict()
    order["id"] = len(orders) + 1
    order["created"] = datetime.now(timezone.utc)
    orders.append(order)
    return_order = deepcopy(order)
    return_order.update({"books": [{"book_id": 1, "quantity": 1}]})
    return return_order
