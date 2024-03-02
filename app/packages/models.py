import atexit
import datetime
import os
import uuid
from typing import Type
from sqlalchemy import create_engine, String, DateTime, func, ForeignKey, UUID
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "753951")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(70), nullable=False)

    token: Mapped['Token'] = relationship('Token', back_populates='user', cascade="all, delete-orphan")
    ads: Mapped['Ad'] = relationship('Ad', back_populates='user', cascade="all, delete-orphan")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, server_default=func.gen_random_uuid(), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(User, back_populates='token')

    @property
    def dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id
        }


class Ad(Base):
    __tablename__ = 'ads'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    owner: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship(User, back_populates='ads')

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "registration_time": self.registration_time.isoformat(),
            "owner": self.user.name
        }


MODEL_TYPE = Type[User | Token | Ad]
MODEL = User | Token | Ad

Base.metadata.create_all(engine)
