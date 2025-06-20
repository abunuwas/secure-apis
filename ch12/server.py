import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

import fastapi
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status

from auth import UserClaims, authorize_access, create_access_token
from db_session import session_maker
from models import Student, Course, Lesson, CourseRegistration, Voucher

server = fastapi.FastAPI()


class Credentials(BaseModel):
    email: str
    password: str


class RegisterStudent(Credentials):
    first_name: str
    last_name: str
    date_birth: datetime
    phone_number: str
    address: str


class GetStudent(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    date_birth: datetime
    email: str
    phone_number: str
    address: str
    registration_voucher: str
    voucher_used: bool


def register_new_student(student_profile: RegisterStudent, db_session: Session):
    student = Student(**student_profile.dict())
    db_session.add(student)
    db_session.commit()
    voucher = Voucher(code=str(uuid.uuid4()), used=False, student_id=student.id)
    db_session.add(voucher)
    db_session.commit()
    return student, voucher


@server.post("/students/register", response_model=GetStudent)
def register_student(student_profile: RegisterStudent):
    with session_maker() as session:
        student, voucher = register_new_student(
            student_profile=student_profile, db_session=session
        )
        return student.dict()


@server.post("/students/login")
def login(credentials: Credentials):
    with session_maker() as session:
        student = session.scalar(
            select(Student).where(
                Student.email == credentials.email,
                Student.password == credentials.password,
            )
        )
        if student is not None:
            return {"access_token": create_access_token(str(student.id))}


class LessonDetail(BaseModel):
    id: UUID
    title: str


class GetCourse(BaseModel):
    id: UUID
    title: str
    instructor: str
    rating: float
    price: float
    lessons: list[LessonDetail]


class ListCourses(BaseModel):
    courses: list[GetCourse]
    total: int


class GetLesson(BaseModel):
    id: UUID
    title: str
    instructor: str
    content: str


class GetCourseRegistrationConfirmation(BaseModel):
    id: UUID
    course_id: UUID
    student: Optional[GetStudent] = None


class CourseRegistrationDetails(BaseModel):
    voucher: Optional[str]
    card_number: str
    cvv: int
    expiry_date: str


class ListStudents(BaseModel):
    students: list[GetStudent]
    total: int


@server.get("/courses", response_model=ListCourses)
async def list_courses(page: int, per_page: int):
    with session_maker() as session:
        courses = session.scalars(select(Course))
        count = session.execute(
            select(func.count()).select_from(select(Course.id).subquery())
        ).scalar_one()
        return {"courses": [course.dict() for course in courses], "total": count}


@server.get("/courses/{course_id}", response_model=GetCourse)
async def get_course_details(course_id: UUID):
    with session_maker() as session:
        course = session.scalar(select(Course).where(Course.id == course_id))
        return course.dict()


@server.get("/courses/{course_id}/lessons/{lesson_id}", response_model=GetLesson)
async def get_lesson(course_id: UUID, lesson_id: UUID):
    with session_maker() as session:
        lesson = session.scalar(
            select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id)
        )
        return lesson.dict()


@server.post(
    "/courses/{course_id}/register",
    response_model=GetCourseRegistrationConfirmation,
    status_code=status.HTTP_201_CREATED,
)
async def register_course(
    course_id: UUID,
    registration_details: CourseRegistrationDetails,
    user_claims: UserClaims = Depends(authorize_access),
):
    with session_maker() as session:
        registration = CourseRegistration(
            student_id=user_claims.sub, course_id=course_id
        )

        if registration_details.voucher:
            voucher = session.scalar(
                select(Voucher).where(Voucher.code == registration_details.voucher)
            )
            if voucher:
                voucher.used = True

        session.add(registration)
        session.commit()

        return registration.dict()


@server.get("/admin/students", response_model=ListStudents)
async def list_students(user_claims: UserClaims = Depends(authorize_access)):
    with session_maker() as session:
        students = session.scalars(select(Student))
        count = session.execute(
            select(func.count()).select_from(select(Course.id).subquery())
        ).scalar_one()
        return {
            "students": [student.dict() for student in students],
            "total": count,
        }


class PersonalDetails(GetStudent):
    course_registrations: list[GetCourseRegistrationConfirmation]


@server.get("/me")
def get_personal_details(user_claims: UserClaims = Depends(authorize_access)):
    with session_maker() as session:
        student = session.scalar(select(Student).where(Student.id == user_claims.sub))
        return student.dict(include_registrations=True)


@server.get(
    "/registrations/{registration_id}", response_model=GetCourseRegistrationConfirmation
)
def get_registration_details(
    registration_id: UUID, user_claims: UserClaims = Depends(authorize_access)
):
    with session_maker() as session:
        registration = session.scalar(select(CourseRegistration))
        return registration.dict(include_student=True)
