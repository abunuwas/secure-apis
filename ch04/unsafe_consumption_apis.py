import enum
import uuid
from typing import Optional

import requests
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select, Uuid, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

server = FastAPI()


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class CharacterModel(Base):
    __tablename__ = "character"

    name: Mapped[str]
    status: Mapped[Optional[str]]


engine = create_engine("sqlite:///unsafe_consumption.db", echo=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


fixture_characters = [
    {
        "name": "Harry Potter",
    },
    {
        "name": "Hermione Granger",
        "status": "witch",
    },
    {
        "name": "Petunia Dursley",
        "status": "muggle",
    },
]

with session_maker() as session:
    if not list(session.scalars(select(CharacterModel))):
        characters = [
            CharacterModel(**character_details)
            for character_details in fixture_characters
        ]
        session.add_all(characters)
        session.commit()


@server.get("/server-a/unsafe-api")
def unsafe_api():
    return {"status": "';--"}


@server.get("/server-b/unsafe-consumption")
def unsafe_consumption():
    status = requests.get("http://localhost:8000/server-a/unsafe-api").json()["status"]
    with session_maker() as session:
        session.execute(
            text(
                f"update character set status = '{status}' "
                f"where name = 'Harry Potter'"
            )
        )
        session.commit()


class StatusEnum(str, enum.Enum):
    wizard = "wizard"
    witch = "witch"
    muggle = "muggle"


class CharacterStatus(BaseModel):
    status: StatusEnum


@server.get("/server-b/safe-consumption")
def safe_consumption():
    status = requests.get("http://localhost:8000/server-a/unsafe-api").json()
    status_validated = CharacterStatus(status=status)
    with session_maker() as session:
        session.execute(
            text(
                f"update character set status = '{status_validated.status}' "
                f"where name = 'Harry Potter'"
            )
        )
        session.commit()


@server.get("/server-b/characters")
def list_characters():
    with session_maker() as session:
        characters = list(session.scalars(select(CharacterModel)))
        return {"characters": characters}
