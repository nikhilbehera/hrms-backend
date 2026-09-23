from pydantic import BaseModel,EmailStr, ConfigDict
from datetime import date, time


class EmployeeCreate(BaseModel):
    name:str
    email:EmailStr
    age:int
    department_id: int

class EmployeeResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    age:int
    department_id: int

    model_config = ConfigDict(from_attributes=True)

class DepartmentCreate(BaseModel):
    name:str
    description:str

class DepartmentResponse(BaseModel):
    id:int
    name:str
    description:str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email:EmailStr
    password:str

class LoginRequest(BaseModel):
    email:EmailStr
    password: str

class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in: time
    check_out: time | None = None
    status: str

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    check_in: time
    check_out: time | None
    status: str

    model_config = ConfigDict(from_attributes=True)

class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class LeaveStatusUpdate(BaseModel):
    status: str


class PayrollCreate(BaseModel):
    employee_id: int
    month: str
    basic_salary: float
    allowance: float = 0
    deduction: float = 0


class PayrollResponse(BaseModel):
    id: int
    employee_id: int
    month: str
    basic_salary: float
    allowance: float
    deduction: float
    net_salary: float

    model_config = ConfigDict(from_attributes=True)

    