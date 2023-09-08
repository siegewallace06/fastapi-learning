from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "test": 70
    },
    2: {
        "name": "Jane",
        "age": 16,
        "test": 80
    }
}

# I believe this is something like DTO in FastAPI


class Student(BaseModel):
    name: str
    age: int
    test: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    test: Optional[int] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student_by_id(student_id: int = Path(description="The ID of the student you want to view", gt=0)):
    # If student_id is not in students, it will return 404 automatically on the response code
    if student_id not in students:
        return {"Error": "Student not found"}

    return students[student_id]


@app.get("/get-student-by-name/{student_id}")
def get_student_by_name(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return {"Data": students[student_id]}
    return {"Data": "Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}

    students[student_id] = student
    return {
        "Success": "Student created",
        "Data": students[student_id]
    }


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    # Only insert the value from the UpdateStudent if it is not None
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.test != None:
        students[student_id].test = student.test

    return {
        "Success": "Student updated",
        "Data": students[student_id]
    }


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    del students[student_id]
    return {"Success": "Student deleted"}
