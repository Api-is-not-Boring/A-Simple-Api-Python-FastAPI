from fastapi import APIRouter, Request, HTTPException, status
from app.model.v2 import *

router = APIRouter(prefix="/api/v2")


@router.on_event("startup")
def on_startup():
    db_init()


@router.get("/cars", response_model=Cars | V2Message)
async def get_cars(request: Request, id: int = None):
    with Session(engine) as session:
        if id:
            car = session.get(Car, id)
            return v2_message(request, "with JSON", car)
        else:
            cars = session.exec(select(Car)).all()
            return Cars(total=len(cars), cars=cars)


@router.post("/cars", response_model=V2Message, status_code=status.HTTP_201_CREATED)
async def create_car(request: Request, input_car: Car):
    with Session(engine) as session:
        session.add(input_car)
        session.commit()
        session.refresh(input_car)
        return v2_message(request, "with JSON", input_car)


@router.put("/cars", response_model=V2Message, response_model_exclude_none=True)
async def update_car(request: Request, input_car: Car, id: int = None):
    with Session(engine) as session:
        if id:
            car = session.get(Car, id)
        else:
            car = session.get(Car, input_car.id)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        for k, v in input_car.dict(exclude_none=True).items():
            setattr(car, k, v)
        session.add(car)
        session.commit()
        session.refresh(car)
        return v2_message(request, "with JSON", car)


@router.delete("/cars", response_model=V2DeleteMessage, response_model_exclude_none=True)
async def delete_car(request: Request, id: int = None):
    with Session(engine) as session:
        car = session.get(Car, id)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(car)
        session.commit()
        total = len(session.exec(select(Car)).all())
        return v2_delete_message("Query Parameter", id, total)


@router.get("/cars/{car_id}", response_model=V2Message, response_model_exclude_none=True)
async def get_car(car_id: int, request: Request):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return v2_message(request, "with Path Parameter", car)


@router.put("/cars/{car_id}", response_model=V2Message, response_model_exclude_none=True)
async def update_car(car_id: int, request: Request, input_car: Car):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        for k, v in input_car.dict(exclude_none=True).items():
            setattr(car, k, v)
        session.add(car)
        session.commit()
        session.refresh(car)
        return v2_message(request, "with Path Parameter", car)


@router.delete("/cars/{car_id}", response_model=V2DeleteMessage, response_model_exclude_none=True)
async def delete_car(car_id: int, request: Request):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(car)
        session.commit()
        total = len(session.exec(select(Car)).all())
        return v2_delete_message("Path Parameter", car_id, total)
