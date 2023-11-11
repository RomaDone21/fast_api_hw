from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {"message": "Hello, World!"}


@app.post("/post")
def get_post():
    return post_db


@app.get("/dog")
def get_dogs(kind: DogType = Query(None, title="Kind of Dog", description="Filter dogs by kind")):
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    else:
        return list(dogs_db.values())


@app.post("/dog")
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=422, detail="Dog with this pk already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail="Dog not found")
    return dogs_db[pk]


@app.patch("/dog/{pk}")
def update_dog(pk: int, updated_dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail="Dog not found")
    dogs_db[pk] = updated_dog
    return updated_dog