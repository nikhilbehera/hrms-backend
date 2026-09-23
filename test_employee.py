from  database import SessionLocal
from models import Employee

db = SessionLocal()

employee = Employee(
    name  ="nikhil",
    email = "nikhil@example.com",
    age = 25
)

db.add(employee)
db.commit()

print ("Employee add successfully")
db.close()