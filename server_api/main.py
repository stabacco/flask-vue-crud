import black
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Python Formatter Api", description="python formatter")


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class Formatters(Enum):
    BLACK = "black"
    YAPF = "yapf"
    AUTOPEP8 = "autopep8"
    DOCFORMATTER = "docformatter"


# class BlackParameters(BaseModel):
#     line_length: int = 79


class FormattableCode(BaseModel):
    code: str
    formatter: str = "black"
    parameters: dict = None


app = FastAPI()


def run_black(code, **kwargs):
    return black.format_str(code, mode=black.FileMode(**kwargs))


def run_docformatter(code, **kwargs):
    import docformatter

    return docformatter.format_code(code, **kwargs)


@app.options('/items/')
async def who_knows_why_i_need_this():
    print('who knows what to do ')
    headers = {"Access-Control-Allow-Origin": "*", 
     'Access-Control-Allow-Headers': '*',
    "Content-Language": "en-US"}
    return JSONResponse(content={}, headers=headers)

@app.post("/items/")
async def create_item(item: FormattableCode):
    item_dict = item.dict()
    code = item_dict["code"]
    formatter = item_dict["formatter"]
    parameters = item_dict["parameters"]

    print("code", code)

    # format with black
    if item_dict["formatter"] == "black":
        formatter = run_black

    # format with docformatter
    elif item_dict["formatter"] == "docformatter":
        formatter = run_docformatter
    else:
        raise HTTPException(status_code=400, detail="not yet implemented")

    try:
        formatted = formatter(code, **parameters)
        item_dict["code"] = formatted

        print("*" * 30)
        print(formatted)
        print("*" * 30)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e), headers={"X-Error": "formatter-error", "Access-Control-Allow-Origin": "*",}
        )
    headers = {"Access-Control-Allow-Origin": "*", 
    "Content-Language": "en-US"}
    return JSONResponse(content=item_dict, headers=headers)
    return item_dict


def params_test(*, some, other, valu=None, forme):
    print(some,valu,)