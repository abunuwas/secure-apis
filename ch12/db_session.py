import uuid
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from models import (
    Base,
    Student,
    Instructor,
    Course,
    Lesson,
    Voucher,
    CourseRegistration,
)

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)

fixture_students = [
    {
        "email": "sarah.connor@apithreats.com",
        "password": "sarah.connor",
        "first_name": "Sarah",
        "last_name": "Connor",
        "date_birth": datetime(1964, 1, 1),
        "phone_number": "+44-2907-361-741",
        "address": "Gilmore Hamlin Apartments - 11844 Hamlin Street, Los Angeles, California, USA.",
    },
    {
        "email": "harry.potter@apithreats.com",
        "password": "harry.potter",
        "first_name": "Harry",
        "last_name": "Potter",
        "date_birth": datetime(1980, 7, 31),
        "phone_number": "+44-2907-361-741",
        "address": "12 Picket Post Close, Bracknell, Berkshire, UK.",
    },
    {
        "email": "frodo.baggins@apithreats.com",
        "password": "frodo.baggins",
        "first_name": "Frodo",
        "last_name": "Baggins",
        "date_birth": datetime(2968, 9, 22),
        "phone_number": "+44-2907-361-741",
        "address": "Bag End, Hobbiton, The Shire",
    },
    {
        "email": "arya.stark@apithreats.com",
        "password": "arya.stark",
        "first_name": "Arya",
        "last_name": "Stark",
        "date_birth": datetime(289, 1, 1),
        "phone_number": "+44-2907-361-741",
        "address": "Winterfell",
    },
    {
        "email": "thomas.anderson@apithreats.com",
        "password": "thomas.anderson",
        "first_name": "Thomas",
        "last_name": "Anderson",
        "date_birth": datetime(1971, 9, 13),
        "phone_number": "+44-2907-361-741",
        "address": "Apartment 101",
    },
]

fixture_instructors = [
    {
        "name": "Jose Haro Peralta",
    },
    {
        "name": "Albus Dumbledore",
    },
]

fixture_course = {
    "title": "Fundamentals of API security",
    # "instructor_id": "mapped_column(ForeignKey("instructor.id"), ondelete="CASCADE")",
    "rating": 10,
    "price": 10,
}

fixture_lessons = [
    {
        "title": "What is API security?",
        "content": "Lorem ipsum dolor sit amet",
        # "instructor_id": "mapped_column(ForeignKey("instructor.id"), ondelete="CASCADE")",
        # "course_id": "mapped_column(ForeignKey("course.id"), ondelete="CASCADE")",
    },
    {
        "title": "Aligning API security with your organization",
        "content": "Lorem ipsum dolor sit amet",
        # "instructor_id": "mapped_column(ForeignKey("instructor.id"), ondelete="CASCADE")",
        # "course_id": "mapped_column(ForeignKey("course.id"), ondelete="CASCADE")",
    },
    {
        "title": "API security principles",
        "content": "Lorem ipsum dolor sit amet",
        # "instructor_id": "mapped_column(ForeignKey("instructor.id"), ondelete="CASCADE")",
        # "course_id": "mapped_column(ForeignKey("course.id"), ondelete="CASCADE")",
    },
    {
        "title": "Top API authentication and authorization vulnerabilities",
        "content": "Lorem ipsum dolor sit amet",
        # "instructor_id": "mapped_column(ForeignKey("instructor.id"), ondelete="CASCADE")",
        # "course_id": "mapped_column(ForeignKey("course.id"), ondelete="CASCADE")",
    },
]


with session_maker() as session:
    if not list(session.scalars(select(Student))):
        students = [Student(**student) for student in fixture_students]
        session.add_all(students)
        session.commit()
    else:
        students = session.scalars(select(Student))

    for student in students:
        if not student.voucher:
            student.voucher = Voucher(code=uuid.uuid4(), used=False)
        session.commit()

    if not list(session.scalars(select(Instructor))):
        instructors = [Instructor(**instructor) for instructor in fixture_instructors]
        session.add_all(instructors)
        session.commit()
    else:
        instructors = list(session.scalars(select(Instructor)))

    if not session.scalar(select(Course)):
        course = Course(**fixture_course, instructor_id=instructors[0].id)
        session.add(course)
        session.commit()
    else:
        course = session.scalar(select(Course))

    if not session.scalar(select(CourseRegistration)):
        for student in students:
            registrations = [
                CourseRegistration(student_id=student.id, course_id=course.id)
            ]
            session.add_all(registrations)
            session.commit()

    if not list(session.scalars(select(Lesson))):
        lessons = [
            Lesson(**lesson, instructor_id=instructors[0].id, course_id=course.id)
            for lesson in fixture_lessons
        ]
        session.add_all(lessons)
        session.commit()
