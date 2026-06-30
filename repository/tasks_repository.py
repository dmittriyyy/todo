from sqlalchemy.orm import Session

from models.tasks import Tasks
from schemas.tasks_schema import TaskCreateSchema, TaskSchema, TaskUpdateDoneSchema, TaskUpdateSchema


def get_all_tasks(db: Session):
    return db.query(Tasks).all()


def get_task_for_id(db: Session, id: int):
    return db.query(Tasks).filter(Tasks.id == id).first()


def create_task(db: Session, task_data: TaskCreateSchema):
    new_task = Tasks(title=task_data.title, description=task_data.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskSchema.model_validate(new_task)


def update_done(db: Session, id: int, update_data: TaskUpdateDoneSchema):
    task = db.query(Tasks).filter(Tasks.id == id).first()

    if task is None:
        return None

    task.done = update_data.done
    db.commit()
    db.refresh(task)
    return TaskSchema.model_validate(task)


def get_done_true(db: Session):
    return db.query(Tasks).filter(Tasks.done == True).all()


def task_update(db: Session, id: int, update_task: TaskUpdateSchema):
    task = db.query(Tasks).filter(Tasks.id == id).first()

    if task is None:
        return None

    task.title = update_task.title
    task.description = update_task.description
    task.done = update_task.done
    db.commit()
    db.refresh(task)
    return task
