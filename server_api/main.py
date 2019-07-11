import black
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


from fastapi import FastAPI
from pydantic import BaseModel


class BlackParameters(BaseModel):
    line_length=79


class FormattableCode(BaseModel):
    code: str
    parameters: BlackParameters = None


app = FastAPI()

def run_black(code):
    return black.format_str(code, mode=black.FileMode())

@app.post("/items/")
async def create_item(item: FormattableCode):
    item_dict = item.dict()
    formatted = run_black(item_dict['code'])
    item_dict['code'] =formatted
    return item_dict
