import json
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Uuid, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from starlette import status
from starlette.requests import Request

server = FastAPI()


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class PaymentModel(Base):
    __tablename__ = "payment"

    amount: Mapped[float]
    currency: Mapped[str]
    status: Mapped[str] = mapped_column(default="pending")


class MakePaymentSchema(BaseModel):
    amount: float
    currency: str


class PaymentSchema(MakePaymentSchema):
    id: uuid.UUID
    status: str


engine = create_engine("sqlite:///mass_assignment.db")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


@server.post(
    "/payments-vulnerable",
    response_model=PaymentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def make_payment(request: Request):
    with session_maker() as session:
        payload = await request.body()
        payment = PaymentModel(**json.loads(payload))
        session.add(payment)
        session.commit()
        return {
            "id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
        }


@server.post(
    "/payments-safe",
    response_model=PaymentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def make_payment(payment_details: MakePaymentSchema):
    with session_maker() as session:
        payment = PaymentModel(**payment_details.dict())
        session.add(payment)
        session.commit()
        return {
            "id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
        }
