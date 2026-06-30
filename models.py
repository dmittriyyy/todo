from sqlalchemy import Boolean, Column, Integer, String

from bd import Base, engine


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)


Base.metadata.create_all(engine)
