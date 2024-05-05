from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]


@app.get("/blog")
def index(limit:int, published: Optional[bool]=False, sort: Optional[str]=None):
  if published:
    return {'data':f"{limit} published blogs from db"}
  return {"data":f"{limit} blog from list"}

@app.get("/blog/unpublished")
def unpublished():
  return {"data":"all unpublished blogs"}

@app.get("/blog/{id}")
def about(id: int):
  return {"data":id}

@app.get("/blog/{id}/comments")
def comments(id: int, limit: int =10):
  return {"data":{"1","2"}}


@app.post("/blog")
def create_blog(request: Blog):
  
  return {"data":f"Blog is created with title at {request.title}"}