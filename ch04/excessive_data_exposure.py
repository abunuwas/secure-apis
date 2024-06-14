import uuid

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Uuid, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

server = FastAPI()


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class ProjectModel(Base):
    __tablename__ = "project"

    title: Mapped[str]


class UserModel(Base):
    __tablename__ = "user"

    email: Mapped[str]
    project: Mapped[str]
    full_name: Mapped[str]


class GetUserProfileSchema(BaseModel):
    email: str
    full_name: str
    project: str


engine = create_engine("sqlite:///excessive_data_exposure.db")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)

fixture_users = [
    {
        "full_name": "Sarah Connor",
        "email": "sarah@apithreats.com",
        "project": "Terminator",
    },
    {"full_name": "Neo Anderson", "email": "neo@apithreats.com", "project": "Matrix"},
]

with session_maker() as session:
    if not list(session.scalars(select(UserModel))):
        users = [UserModel(**user_details) for user_details in fixture_users]
        session.add_all(users)
        session.commit()


class UserClaims(BaseModel):
    sub: str
    project: str


def validate_access():
    return UserClaims(sub=str(uuid.uuid4()), project="Matrix")


@server.get(
    "/query-user-vulnerable",
    response_model=GetUserProfileSchema,
)
async def query_user_vulnerable(
    email: str, user_claims: UserClaims = Depends(validate_access)
):
    with session_maker() as session:
        user = session.scalar(select(UserModel).where(UserModel.email == email))
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with email {email} not found."
            )
        return {
            "email": user.email,
            "project": user.project,
            "full_name": user.full_name,
        }


@server.get(
    "/query-user-safe",
    response_model=GetUserProfileSchema,
)
async def query_user_safe(
    email: str, user_claims: UserClaims = Depends(validate_access)
):
    with session_maker() as session:
        user = session.scalar(
            select(UserModel).where(
                UserModel.email == email,
                UserModel.project == user_claims.project,
            )
        )
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with email {email} not found."
            )
        return {
            "id": user.id,
            "email": user.email,
            "project": user.project,
            "full_name": user.full_name,
        }
