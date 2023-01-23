from fastapi import FastAPI, Query, Body
from typing import Union, List
from datetime import datetime, time, timedelta
from uuid import UUID
from ninjadog import render

from mod.MyPyDB import setDB, db

app = FastAPI()

setDB('127.0.0.1', 'aut', '** yes: i am an author **', 'jagoda')

@app.get("/")
async def root():
    print('working ...')
    return {"message": "Hello World"}

@app.get("/test1")
async def test1():
    db().test1()
    return {"message": "test1"}

@app.get("/test2")
async def test2():
    db().test2()
    return {"message": "test2"}

# @app.get("/items/{item_id}")
# async def read_item(item_id:int):
#     return {"item_id": item_id}

@app.get("/files/{file_path:path}")
async def read_file(file_path:str):
    return {"file_path": file_path} 

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# @app.get("/items/")
# async def read_item(skip:int=0, limit:int=10):
#     return fake_items_db[skip:skip + limit]
#> http://127.0.0.1:8000/items/?skip=0&limit=10


# @app.get("/items/{item_id}")
# async def read_item(item_id:str, q:Union[str, None]=None):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     return item
#> http://127.0.0.1:8000/items/foo?q=hello

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item:Item):
    return item

@app.get("/items/")
async def read_items(q:List[str]=Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items
# http://127.0.0.1:8000/items/?q=a&q=b&q=hello%20world

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
#    curl -X 'PUT' \
#   'http://127.0.0.1:8000/items/6B29FC40-CA47-1067-B31D-00DD010662DA' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "start_datetime": "2023-01-16T13:19:52.896Z",
#   "end_datetime": "2023-01-16T13:19:52.896Z",
#   "repeat_at": "string",
#   "process_after": 0
# }'