from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "test": 70
    }
}


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
