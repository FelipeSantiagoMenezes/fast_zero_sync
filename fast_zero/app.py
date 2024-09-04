from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routes import auth, users
from fast_zero.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/hello/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_hello():
    return '<h1>Olá mundo!<h1>'
