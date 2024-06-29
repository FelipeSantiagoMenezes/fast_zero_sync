from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Menssage

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Menssage)
def root():
    return {'mensage': 'Olá mundo!', 'batata': 'batata'}


@app.get('/hello/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello():
    return 'Olá mundo!'
