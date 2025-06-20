import uuid

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auth import UserClaims, validate_access


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


@server.get("/vulnerable/orders/{order_id}")
def vulnerable_get_order_details(
    order_id: uuid.UUID, user_claims: UserClaims = Depends(validate_access)
):
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
def get_order_details(
    order_id: int, user_claims: UserClaims = Depends(validate_access)
):
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
