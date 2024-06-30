from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    Message,
    UserDB,
    UserPublic,
    UserSchema,
    UsersList,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/hello/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_hello():
    return 'Olá mundo!'


@app.get('/users/', response_model=UsersList)
def read_users():
    return {'users': database}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(ID=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def uptade_user(user_id: int, user: UserSchema):
    if 1 > user_id or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(ID=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if 1 > user_id or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted!'}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    if 1 > user_id or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]
