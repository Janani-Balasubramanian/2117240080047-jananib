from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

items: List[Item] = []

@app.post('/items', response_model=Item)
def create_item(item: Item):
    if any(existing.id == item.id for existing in items):
        raise HTTPException(status_code=400, detail='Item already exists')
    items.append(item)
    return item

@app.get('/items', response_model=List[Item])
def list_items():
    return items

@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail='Not found')

@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, updated: Item):
    for idx, item in enumerate(items):
        if item.id == item_id:
            items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail='Not found')
