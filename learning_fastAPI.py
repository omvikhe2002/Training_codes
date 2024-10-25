from fastapi import FastAPI,Path
from pydantic import BaseModel
from typing import Optional

app=FastAPI()
students={
    1:{
        "name":"Om",
        "age":22,
        "proffesion":"Engineer"
    }
}

#THIS IS REQUIRED FOR POST METHOD
class Student(BaseModel):
    name:str
    age:int
    proffesion:str

class UpdateStudent(BaseModel):
    name: Optional[str]= None
    age: Optional[int]= None
    year: Optional[str]= None

# PATH PARAMETERS
@app.get("/get-student/{student_id}")
def get_student(student_id:int= Path(..., description="The ID of the student you want to view",gt=0, lt=3)):  #this will give the good description inthe final output   2)gt=greater than 3)lt=less than
    return students[student_id]

# QUERY PARAMETERS
@app.get("/get-by-age/{student_id}")
def get_student(*,student_id:int, age:Optional[int]=None):
    for student_id in students:
        if  students[student_id]["age"]==age:
            return students[student_id]
    return {"Data":"Not Found"}


#  POST METHOD
@app.post("/create-student/{student_id}")
def create_student(student_id:int, student:Student):
    if student_id in students:
        return {"Error":"Student exsists"}

    students[student_id]=student
    return students[student_id]

#PUT METHOD
@app.put("/update-student/{student_id}")
def update_student(student_id:int, student:Student):
    if student_id not in students:
        return{"Error":"Student does not exsist"}

    if student.name != None:
        students[student_id].name=student.name

    if student.age !=None:
        students[student_id].age=student.age

    if student.profession != None:
        students[student_id].profession=student.profession

    return students[student_id]

#DELETE METHOD
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return{"Error":"Student does not exist"}

    del students[student_id]
    return {"Message":"Student deleted successfully"}
            
if __name__=="__main__":
    import uvicorn
    uvicorn.run("learning_fastAPI:app", host="127.0.0.1", port=8001, reload=True)