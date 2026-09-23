from database import Base, engine
from models import Employee, Department, User, Attendance, Leave, Payroll

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")