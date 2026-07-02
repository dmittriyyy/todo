from sqlalchemy.orm import Session

from models.tasks import Tasks
from schemas.tasks_schema import (
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateDoneSchema,
    TaskUpdateSchema,
)


def get_all_tasks(db: Session, user_id: int):
    return db.query(Tasks.user_id == user_id).all()


def get_task_for_id(db: Session, task_id: int, user_id: int):
    return db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user_id).first()


def create_task(db: Session, task_data: TaskCreateSchema, user_id: int):
    new_task = Tasks(
        title=task_data.title,
        description=task_data.description,
        date_to=task_data.date_to,
        user_id=user_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskSchema.model_validate(new_task)


def update_done(
    db: Session, task_id: int, user_id: int, update_data: TaskUpdateDoneSchema
):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user_id).first()

    if task is None:
        return None

    task.done = update_data.done
    db.commit()
    db.refresh(task)
    return TaskSchema.model_validate(task)


def get_done_true(db: Session, user_id: int):
    return db.query(Tasks).filter(Tasks.done == True, Tasks.user_id == user_id).all()


def task_update(db: Session, task_id: int, user_id: int, update_task: TaskUpdateSchema):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user_id).first()

    if task is None:
        return None

    task.title = update_task.title
    task.description = update_task.description
    task.date_to = update_task.date_to

    db.commit()
    db.refresh(task)
    return TaskSchema.model_validate(task)
