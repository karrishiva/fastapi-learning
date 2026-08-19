from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.schemas.todos import TodoCreate, TodoResponse, TodoUpdate, TodoListResponse
from app.dependencies import get_db
from app.models.todo import Todo

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return {"todos": todos}


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    for key, value in todo.model_dump().items():
        setattr(existing_todo, key, value)

    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo_partial(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db)
):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    update_data = todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_todo, key, value)

    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()
    return None