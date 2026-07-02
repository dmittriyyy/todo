from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm.session import Session

from bd import Base, engine, get_db
from repository.tasks_repository import (
    create_task,
    get_all_tasks,
    get_done_true,
    get_task_for_id,
    task_update,
    update_done,
)
from schemas.tasks_schema import (
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateDoneSchema,
    TaskUpdateSchema,
)

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/tasks", response_model=TaskSchema)
def add_task(task: TaskCreateSchema, db: Session = Depends(get_db)):
    try:
        return create_task(db, task)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось создать задачу") from e


@app.get("/all_tasks", response_model=list[TaskSchema])
def all_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)


@app.get("/tasks/done", response_model=list[TaskSchema])
def ready_tasks(db: Session = Depends(get_db)):
    return get_done_true(db)


@app.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return get_task_for_id(db, task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Задача не найдена") from e


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def done_update(
    task_id: int, task: TaskUpdateDoneSchema, db: Session = Depends(get_db)
):
    result = update_done(db, task_id, task)

    if result is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return result


@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int, new_data: TaskUpdateSchema, db: Session = Depends(get_db)
):
    result = task_update(db, task_id, new_data)

    if result is None:
        raise HTTPException(status_code=404, detail="Не удалось обновить данные")

    return result
