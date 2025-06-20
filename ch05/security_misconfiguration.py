import uuid
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Uuid, select, text
from sqlalchemy.orm import sessionmaker, Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class UserModel(Base):
    __tablename__ = "user"

    name: Mapped[str]
    email: Mapped[str]


engine = create_engine("sqlite:///security_misconfiguration.db")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


fixture_users = [
    {
        "name": "Sarah Connor",
        "email": "sarah@apithreats.com",
    },
    {
        "name": "Neo Anderson",
        "email": "neo@apithreats.com",
    },
]

with session_maker() as session:
    if not list(session.scalars(select(UserModel))):
        users = [UserModel(**user_details) for user_details in fixture_users]
        session.add_all(users)
        session.commit()


server = FastAPI(debug=True)


class UserSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str


class ListUsersSchema(BaseModel):
    users: list[UserSchema]


@server.get("/users", response_model=ListUsersSchema)
def list_users(order_by: Optional[str] = "email"):
    with session_maker() as session:
        users = list(session.scalars(select(UserModel).order_by(text(order_by))))
        return {"users": users}
