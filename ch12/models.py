from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import MetaData, Uuid, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s_idx",
            "uq": "uq_%(table_name)s_%(column_0_name)s_key",
            "ck": "ck_%(table_name)s_%(constraint_name)s_check",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
            "pk": "pk_%(table_name)s_pkey",
        }
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda _: datetime.now(timezone.utc)
    )


class Student(Base):
    __tablename__ = "student"

    email: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_birth: Mapped[datetime]
    phone_number: Mapped[str]
    address: Mapped[str]

    voucher: Mapped["Voucher"] = relationship()
    course_registrations: Mapped[List["CourseRegistration"]] = relationship()

    def dict(self, include_registrations=False):
        details = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_birth": self.date_birth,
            "phone_number": self.phone_number,
            "address": self.address,
            "registration_voucher": self.voucher.code,
            "voucher_used": self.voucher.used,
        }
        if include_registrations:
            registrations = [
                registration.dict() for registration in self.course_registrations
            ]
            details.update({"course_registrations": registrations})
        return details


class Voucher(Base):
    __tablename__ = "voucher"

    code: Mapped[str]
    used: Mapped[bool]
    student_id = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))


class CourseRegistration(Base):
    __tablename__ = "course_registration"

    student_id = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    course_id = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))

    student: Mapped["Student"] = relationship()

    def dict(self, include_student: bool = False):
        details = {
            "id": self.id,
            "course_id": self.course_id,
        }
        if include_student:
            details.update({"student": self.student.dict()})
        return details


class Instructor(Base):
    __tablename__ = "instructor"

    id: Mapped[str]
    name: Mapped[str]


class Course(Base):
    __tablename__ = "course"

    title: Mapped[str]
    instructor_id = mapped_column(ForeignKey("instructor.id", ondelete="CASCADE"))
    rating: Mapped[float]
    price: Mapped[float]

    lessons: Mapped[List["Lesson"]] = relationship()
    instructor: Mapped["Instructor"] = relationship()

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructor": self.instructor.name,
            "rating": self.rating,
            "price": self.price,
            "lessons": [
                {
                    "id": lesson.id,
                    "title": lesson.title,
                }
                for lesson in self.lessons
            ],
        }


class Lesson(Base):
    __tablename__ = "lesson"

    title: Mapped[str]
    content: Mapped[str]
    instructor_id = mapped_column(ForeignKey("instructor.id", ondelete="CASCADE"))
    course_id = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))

    instructor: Mapped["Instructor"] = relationship()

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructor": self.instructor.name,
            "content": self.content,
        }
