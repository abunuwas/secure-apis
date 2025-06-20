import uuid
from datetime import datetime, timezone
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, conint
from requests import Request
from starlette import status
from starlette.responses import JSONResponse

server = FastAPI()


tickets_db = [
    {
        "id": UUID("deb6f47e-fd9d-4b4c-ae4f-c85726ed502c"),
        "artist": "Taylor Swift",
        "date": datetime(2025, 6, 17, 18),
        "venue": "Wembley Stadium, London, UK",
        "price": 250,
        "amount_left": 20,
    },
    {
        "id": UUID("13464bd6-981c-42e4-87d3-44476f6deacd"),
        "artist": "Iron Maiden",
        "date": datetime(2025, 5, 22, 19),
        "venue": "O2 Arena, London, UK",
        "price": 250,
        "amount_left": 20,
    },
]


class UserClaims(BaseModel):
    sub: str


def validate_access():
    return UserClaims(sub="deb6f47e-fd9d-4b4c-ae4f-c85726ed502c")


allowed_agents = ["Mozilla", "Google Chrome", "Safari", "Microsoft Edge", "Opera"]


class Transaction(BaseModel):
    sub: str
    date: datetime

    @property
    def within_24h(self):
        time_diff = datetime.now(timezone.utc).timestamp() - self.date.timestamp()
        return (time_diff / 3600) <= 24


recent_transactions: list[Transaction] = []


@server.middleware("http.request")
async def prevent_scalping(request: Request, call_next):
    if not any(agent in request.headers["user-agent"] for agent in allowed_agents):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    user_claims = validate_access()

    if request.url.path == "/checkout":
        for transaction in recent_transactions:
            if transaction.sub == user_claims.sub and transaction.within_24h:
                return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    return await call_next(request)


class Ticket(BaseModel):
    id: UUID
    artist: str
    date: datetime
    venue: str
    price: float
    amount_left: int


class ListTickets(BaseModel):
    tickets: list[Ticket]


class BuyTickets(BaseModel):
    ticket: UUID
    amount: conint(lt=5)


class TicketsPurchase(BaseModel):
    id: UUID
    ticket: Ticket


@server.get("/tickets", response_model=ListTickets)
def list_tickets():
    return {"tickets": tickets_db}


@server.post(
    "/checkout",
    response_model=TicketsPurchase,
    status_code=status.HTTP_201_CREATED,
)
def checkout(
    ticket_details: BuyTickets,
    user_claims: UserClaims = Depends(validate_access),
):
    for ticket in tickets_db:
        if ticket["id"] == ticket_details.ticket:
            recent_transactions.append(
                Transaction(sub=user_claims.sub, date=datetime.now(timezone.utc))
            )
            return {
                "id": uuid.uuid4(),
                "ticket": ticket,
                "amount": ticket_details.amount,
            }
    raise HTTPException(
        status_code=404, detail=f"Ticket with ID {ticket_details.ticket} not found."
    )
