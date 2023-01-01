from typing import Optional
from fastapi import Request
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select

__all__ = [
    "Session",
    "select",
    "Car",
    "Cars",
    "engine",
    "db_init",
    "V2Message",
    "v2_message",
    "V2DeleteMessage",
    "v2_delete_message",
]

engine = create_engine("sqlite://", echo=True)


class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    price: int = Field(...)


class Cars(BaseModel):
    total: int
    cars: list[Car]


init_car = [
    Car(name="Audi", price=52642),
    Car(name="Mercedes", price=57127),
    Car(name="Skoda", price=9000),
    Car(name="Volvo", price=29000),
    Car(name="Bentley", price=350000),
    Car(name="Citroen", price=21000),
    Car(name="Hummer", price=41400),
    Car(name="Volkswagen", price=21600)
]


def db_init():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(init_car)
        session.commit()


class V2Message(BaseModel):
    method: str = Field(...)
    car: Car | None = Field(None)


class V2DeleteMessage(BaseModel):
    message: str = Field(...)
    deleted: int = Field(...)
    total: int = Field(...)


def v2_message(r: Request, m: str, c: Car = None) -> V2Message:
    return V2Message(method="[v2] -> " + r.method + " " + m, car=c)


def v2_delete_message(m: str, d: int, t: int) -> V2DeleteMessage:
    return V2DeleteMessage(message="[v2] -> DELETE " + m, deleted=d, total=t)
