from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    BigInteger,
    String,
    Date,
    ForeignKey,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
import enum


Base = declarative_base()


class Language(enum.Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    UKRAINIAN = "uk"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    name = Column(String, nullable=True)
    language = Column(Enum(Language), default=Language.RUSSIAN)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, date_of_birth={self.date_of_birth}, username='{self.name}')>"


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    recipient_id = Column(BigInteger)
    user = Column(String, ForeignKey("users.telegram_id"))
