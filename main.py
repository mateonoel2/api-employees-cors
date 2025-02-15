from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
import mysql.connector
import schemas

app = FastAPI()

origins = ['*'] # Permite que el Api Rest se consuma desde cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host_name = "172.31.91.211" # IPv4 privada de "MV Bases de Datos"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_employees"  

# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# Get all employees
@app.get("/employees")
def get_employees():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"employees": result}

# Get an employee by ID
@app.get("/employees/{id}")
def get_employee(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM employees WHERE id = {id}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"employee": result}

# Add a new employee
@app.post("/employees")
def add_employee(item:schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    name = item.name
    age = item.age
    cursor = mydb.cursor()
    sql = "INSERT INTO employees (name, age) VALUES (%s, %s)"
    val = (name, age)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee added successfully"}

# Modify an employee
@app.put("/employees/{id}")
def update_employee(id:int, item:schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    name = item.name
    age = item.age
    cursor = mydb.cursor()
    sql = "UPDATE employees set name=%s, age=%s where id=%s"
    val = (name, age, id)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee modified successfully"}

# Delete an employee by ID
@app.delete("/employees/{id}")
def delete_employee(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM employees WHERE id = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee deleted successfully"}
