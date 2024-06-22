from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    guid: Mapped[str] = Column(String, unique=True)
    session_id: Mapped[str] = Column(String)