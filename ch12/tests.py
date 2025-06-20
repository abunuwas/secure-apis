from datetime import datetime

import pytest
from sqlalchemy import select
from starlette_testclient import TestClient

from auth import create_access_token
from db_session import session_maker
from models import Course, CourseRegistration, Student
from server import server, register_new_student, RegisterStudent

client = TestClient(server)


def test_broken_authentication():
    with session_maker() as session:
        course = session.scalar(select(Course))
        lessons = course.lessons
    response = client.get(f"/courses/{course.id}/lessons/{lessons[0].id}")
    assert response.status_code == 403


def test_bola():
    with session_maker() as session:
        student = session.scalar(select(Student))
        registration = session.scalar(
            select(CourseRegistration).where(
                CourseRegistration.student_id != student.id
            )
        )
    token = create_access_token(sub="test")
    response = client.get(
        f"/registrations/{registration.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_rbac():
    token = create_access_token(sub="test")
    response = client.get(
        "/admin/students", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


@pytest.fixture
def new_student_voucher():
    student_details = {
        "first_name": "John",
        "last_name": "Connor",
        "date_birth": datetime(1985, 2, 28),
        "phone_number": "634-430-6045",
        "address": "19828 Valerio Street, Winnetka, CA",
        "email": "john.connor@apithreats.com",
        "password": "john.connor",
    }
    with session_maker() as session:
        student, voucher = register_new_student(
            student_profile=RegisterStudent(**student_details), db_session=session
        )
        return student.id, voucher.code


@pytest.fixture
def course_id():
    with session_maker() as session:
        course = session.scalar(select(Course))
        return course.id


def test_coupon_code_reuse(new_student_voucher, course_id):
    student_id, voucher_id = new_student_voucher
    token = create_access_token(sub=str(student_id))
    registration_payload = {
        "voucher": str(voucher_id),
        "card_number": "5352 6878 8810 6793",
        "cvv": 369,
        "expiry_date": "01/28",
    }
    first_registration = client.post(
        f"/courses/{course_id}/register",
        headers={"Authorization": f"Bearer {token}"},
        json=registration_payload,
    )
    second_registration = client.post(
        f"/courses/{course_id}/register",
        headers={"Authorization": f"Bearer {token}"},
        json=registration_payload,
    )
    assert first_registration.status_code == 201
    assert second_registration.status_code == 409


def test_coupon_abuse(new_student_voucher, course_id):
    new_student_id, new_voucher_id = new_student_voucher
    with session_maker() as session:
        student = session.scalar(select(Student).where(Student.id != new_student_id))
        token = create_access_token(sub=str(student.id))
    registration_payload = {
        "voucher": str(new_voucher_id),
        "card_number": "5352 6878 8810 6793",
        "cvv": 369,
        "expiry_date": "01/28",
    }
    registration = client.post(
        f"/courses/{course_id}/register",
        headers={"Authorization": f"Bearer {token}"},
        json=registration_payload,
    )
    assert registration.status_code == 401
