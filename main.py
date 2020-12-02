from typing import Optional
from typing import List

import base64
from base64 import b64decode
import sys, os, io
import json
from PIL import Image
import pandas as pd
import numpy as np
from pyzbar.pyzbar import decode

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()


class Input(BaseModel):
    base64str : str

def base64str_to_PILImage(base64str):
    base64_img_bytes = base64str.encode('utf-8')
    base64bytes = base64.b64decode(base64_img_bytes)
    bytesObj = io.BytesIO(base64bytes)
    img = Image.open(bytesObj)
    return img

@app.post("/predict")
def get_predictionbase64(tax_image:Input) -> List[str]:
    '''
    FastAPI API will take a base 64 image as input and return a json object
    '''
    # Load the image
    img = base64str_to_PILImage(tax_image.base64str)
    decodedObjects = decode(img)

    # Print results
    bar_code_list=[]
    for obj in decodedObjects:
        bar_code_list.append(obj.data.decode("utf-8") )

    return bar_code_list[::-1]


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
