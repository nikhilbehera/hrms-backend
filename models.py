from sqlalchemy import String, Integer, ForeignKey, Date, Time, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, time

from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)

    department_id:Mapped[int] = mapped_column(
        ForeignKey("department.id")
    )


class Department(Base):
    __tablename__ = "department"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    description:Mapped[str] = mapped_column(String(255))


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100))
    password:Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="employee")

class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    date: Mapped[date] = mapped_column(Date)

    check_in: Mapped[time] = mapped_column(Time)

    check_out: Mapped[time | None] = mapped_column(
        Time,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50)
    )

class Leave(Base):
    __tablename__ = "leaves"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    leave_type: Mapped[str] = mapped_column(
        String(50)
    )

    start_date: Mapped[date] = mapped_column(
        Date
    )

    end_date: Mapped[date] = mapped_column(
        Date
    )

    reason: Mapped[str] = mapped_column(
        String(255)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending"
    )

class Payroll(Base):
    __tablename__ = "payroll"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    month: Mapped[str] = mapped_column(
        String(20)
    )

    basic_salary: Mapped[float] = mapped_column(
        Float
    )

    allowance: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    deduction: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    net_salary: Mapped[float] = mapped_column(
        Float
    )


