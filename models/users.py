from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from bd import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    tasks = relationship("Tasks", back_populates="owner")
