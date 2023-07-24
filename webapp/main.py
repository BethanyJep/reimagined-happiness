import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

DEFAULT_LENGTH = 20


class Body(BaseModel):
    length: Union[int, None] = DEFAULT_LENGTH
    text: str


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    try:
        string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    except Exception as e:
        return {'error': str(e)}
    return {'token': string}


@app.post('/checksum')
def checksum(body: Body):
    """
    Generate a checksum of the text. Example POST request body:

    {
        "text": "Hello World!"
    }
    """
    try:
        checksum = hashlib.sha256(body.text.encode('utf-8')).hexdigest()
    except Exception as e:
        return {'error': str(e)}
    return {'checksum': checksum}