from fastapi import Body, Depends, FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo as TodoModel
from schemas import Todo as TodoSchema, TodoCreate

app = FastAPI()
api = app


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Post request to create a new todo item
@app.post("/todos", response_model=TodoSchema)
def create_todo(todo: TodoCreate = Body(...), db: Session = Depends(get_db)):
    db_todo = TodoModel(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
