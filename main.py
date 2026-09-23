from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Employee, Department, User, Attendance, Leave, Payroll
from schemas import EmployeeCreate, EmployeeResponse, DepartmentCreate,LoginRequest, DepartmentResponse, UserCreate
from password import hash_password, verify_password, check_password
from auth import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import AttendanceCreate, AttendanceResponse, LeaveCreate,PayrollCreate, PayrollResponse, LeaveResponse, LeaveStatusUpdate


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    username = verify_access_token(token)

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return username

def require_role(required_role: str):

    def role_checker(
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(
            User.username == current_user
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        if user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission"
            )

        return user

    return role_checker

@app.get("/")
def home():
    return {
        "message":"HRMS Backend Is Running"
    }

@app.post("/employees")
def create_employee(employee:EmployeeCreate, db:Session = Depends(get_db)):
    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        age=employee.age,
        department_id = employee.department_id
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    employees = db.query(Employee).all()
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id:int, employee:EmployeeCreate, db:Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if existing_employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")

    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.age = employee.age

    db.commit()
    db.refresh(existing_employee)

    return existing_employee




@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}

@app.post("/departments", response_model=DepartmentResponse)
def create_department(
    department:DepartmentCreate,
    db:Session = Depends(get_db)):
    new_department = Department(
        name = department.name,
        description = department.description
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department

@app.get("/departments", response_model=list[DepartmentResponse])
def get_departments(db:Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments

@app.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db:Session = Depends(get_db)
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department Not Found")

    return department

@app.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department:DepartmentCreate,
    db:Session = Depends(get_db)
):
    existing_department = db.query(Department).filter(Department.id == department_id).first()
    if existing_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    existing_department.name = department.name
    existing_department.description = department.description

    db.commit()
    db.refresh(existing_department)

    return existing_department

@app.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}


@app.post("/register")
def register_user(
    user:UserCreate,
    db:Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password,
        role = "employee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email":new_user.email,
        "role": new_user.role
    }

@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(existing_user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_role("admin"))
):
    return {
        "message": "Welcome Admin",
        "username": current_user.username,
        "role": current_user.role
    }


@app.post("/attendance", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    new_attendance = Attendance(
        employee_id = attendance.employee_id,
        date = attendance.date,
        check_in = attendance.check_in,
        check_out = attendance.check_out,
        status = attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance

@app.get("/attendance", response_model=list[AttendanceResponse])
def get_attendance(
    db:Session = Depends(get_db)
):
    attendance_records = db.query(Attendance).all()

    return attendance_records

@app.get("/attendance/employee/{employee_id}", response_model=list[AttendanceResponse])
def get_employee_attendance(
    employee_id: int,
    db:Session = Depends(get_db)
):
    attendance_records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()

    return attendance_records

@app.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    existing_attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not existing_attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    existing_attendance.employee_id = attendance.employee_id
    existing_attendance.date = attendance.date
    existing_attendance.check_in = attendance.check_in
    existing_attendance.check_out = attendance.check_out
    existing_attendance.status = attendance.status

    db.commit()
    db.refresh(existing_attendance)

    return existing_attendance

@app.delete("/attendance/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    existing_attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not existing_attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    db.delete(existing_attendance)
    db.commit()

    return {
        "message": "Attendance deleted successfully"
    }

@app.post("/leaves", response_model=LeaveResponse)
def apply_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):
    new_leave = Leave(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending"
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave

@app.get("/leaves", response_model=list[LeaveResponse])
def get_leaves(
    db: Session = Depends(get_db)
):
    leaves = db.query(Leave).all()

    return leaves

@app.get("/leaves/employee/{employee_id}", response_model=list[LeaveResponse])
def get_employee_leaves(
    employee_id: int,
    db: Session = Depends(get_db)
):
    leaves = db.query(Leave).filter(
        Leave.employee_id == employee_id
    ).all()

    return leaves

@app.put("/leaves/{leave_id}/status", response_model=LeaveResponse)
def update_leave_status(
    leave_id: int,
    status_update: LeaveStatusUpdate,
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    if status_update.status not in ["Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Rejected"
        )

    leave.status = status_update.status

    db.commit()
    db.refresh(leave)

    return leave

@app.post("/payroll", response_model=PayrollResponse)
def create_payroll(
    payroll: PayrollCreate,
    db: Session = Depends(get_db)
):
    net_salary = (
        payroll.basic_salary
        + payroll.allowance
        - payroll.deduction
    )

    new_payroll = Payroll(
        employee_id=payroll.employee_id,
        month=payroll.month,
        basic_salary=payroll.basic_salary,
        allowance=payroll.allowance,
        deduction=payroll.deduction,
        net_salary=net_salary
    )

    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)

    return new_payroll

@app.get("/payroll", response_model=list[PayrollResponse])
def get_payroll(
    db: Session = Depends(get_db)
):
    payroll_records = db.query(Payroll).all()

    return payroll_records

@app.get(
    "/payroll/employee/{employee_id}",
    response_model=list[PayrollResponse]
)
def get_employee_payroll(
    employee_id: int,
    db: Session = Depends(get_db)
):
    payroll_records = db.query(Payroll).filter(
        Payroll.employee_id == employee_id
    ).all()

    return payroll_records

@app.put("/payroll/{payroll_id}", response_model=PayrollResponse)
def update_payroll(
    payroll_id: int,
    payroll: PayrollCreate,
    db: Session = Depends(get_db)
):
    existing_payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if not existing_payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found"
        )

    net_salary = (
        payroll.basic_salary
        + payroll.allowance
        - payroll.deduction
    )

    existing_payroll.employee_id = payroll.employee_id
    existing_payroll.month = payroll.month
    existing_payroll.basic_salary = payroll.basic_salary
    existing_payroll.allowance = payroll.allowance
    existing_payroll.deduction = payroll.deduction
    existing_payroll.net_salary = net_salary

    db.commit()
    db.refresh(existing_payroll)

    return existing_payroll

@app.delete("/payroll/{payroll_id}")
def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    existing_payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if not existing_payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found"
        )

    db.delete(existing_payroll)
    db.commit()

    return {
        "message": "Payroll deleted successfully"
    }