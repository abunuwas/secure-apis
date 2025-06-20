import uuid

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auth import validate_access, UserClaims

server = FastAPI()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(str, primary_key=True, default=uuid.uuid4)


class ProjectModel(Base):
    __tablename__ = "project"

    title: Mapped[str]


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str]
    project: Mapped[str]


class GetUserProfileSchema(BaseModel):
    id: str
    full_name: str
    email: str
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


class SetMeUp(BaseModel):
    project: str
    full_name: str
    email: str


@server.put("/set-me-up", response_model=UserModel)
def set_me_up(
    user_details: SetMeUp, user_claims: UserClaims = Depends(validate_access)
):
    with session_maker() as session:
        user = UserModel(
            id=user_claims.sub,
            project=user_details.project,
            full_name=user_details.full_name,
            email=user_details.email,
        )
        session.add(user)
        session.commit()
        return {
            "id": user.id,
            "email": user.email,
            "project": user.project,
            "full_name": user.full_name,
        }


@server.get(
    "/vulnerable/query-user",
    response_model=GetUserProfileSchema,
)
async def vulnerable_query_user(
    email: str, user_claims: UserClaims = Depends(validate_access)
):
    with session_maker() as session:
        requested_user = session.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        if requested_user is None:
            raise HTTPException(
                status_code=404, detail=f"User with email {email} not found."
            )
        return {
            "id": requested_user.id,
            "email": requested_user.email,
            "project": requested_user.project,
            "full_name": requested_user.full_name,
        }


@server.get(
    "/query-user",
    response_model=GetUserProfileSchema,
)
async def query_user(email: str, user_claims: UserClaims = Depends(validate_access)):
    with session_maker() as session:
        requesting_user = session.scalar(
            UserModel.id == user_claims.sub,
        )
        requested_user = session.scalar(
            select(UserModel).where(
                UserModel.email == email,
                UserModel.project == requesting_user.project,
            )
        )
        if requested_user is None:
            raise HTTPException(
                status_code=404, detail=f"User with email {email} not found."
            )
        return {
            "id": requested_user.id,
            "email": requested_user.email,
            "project": requested_user.project,
            "full_name": requested_user.full_name,
        }
