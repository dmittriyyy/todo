from fastapi import Depends, FastAPI, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from bd import Base, engine, get_db
from models.users import Users
from repository.tasks_repository import (
    create_task,
    get_all_tasks,
    get_done_true,
    get_task_for_id,
    task_del,
    task_update,
    update_done,
)
from repository.users_repository import (
    create_user,
    found_user_by_id,
    found_user_by_login,
)
from schemas.tasks_schema import (
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateDoneSchema,
    TaskUpdateSchema,
)
from schemas.users_schema import UserCreateSchema, UserResponseSchema
from utils.password import hash_password, verify_password
from utils.security import create_token, get_current_user

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/tasks", response_model=TaskSchema)
def add_task(
    task: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        return create_task(db, task, user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось создать задачу") from e


@app.get("/all_tasks", response_model=list[TaskSchema])
def all_tasks(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return get_all_tasks(db, user.id)


@app.get("/tasks/done", response_model=list[TaskSchema])
def ready_tasks(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return get_done_true(db, user.id)


@app.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    try:
        return get_task_for_id(db, task_id, user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Задача не найдена") from e


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def done_update(
    task_id: int,
    task: TaskUpdateDoneSchema,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    result = update_done(db, task_id, user.id, task)

    if result is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return result


@app.delete("/tasks/{task_id}", status_code=204)
def task_delete(
    task_id: int,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    if not task_del(db, task_id, user.id):
        raise HTTPException(status_code=404, detail="Задача не найдена")


@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    new_data: TaskUpdateSchema,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    result = task_update(db, task_id, user.id, new_data)

    if result is None:
        raise HTTPException(status_code=404, detail="Не удалось обновить данные")

    return result


@app.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = found_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return UserResponseSchema.model_validate(user)


@app.post("/auth/register", response_model=UserResponseSchema)
def register(user_create: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = found_user_by_login(db, user_create.name)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким именем существует"
        )

    hash_pass = hash_password(user_create.password)
    new_user = create_user(db, user_create, hash_pass)

    return UserResponseSchema.model_validate(new_user)


@app.post("/auth/login")
def login(
    db: Session = Depends(get_db), user_data: OAuth2PasswordRequestForm = Depends()
):
    user = found_user_by_login(db, user_data.username)
    if not user or not verify_password(user_data.password, str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Неверные логин или пароль")
    token = create_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}
