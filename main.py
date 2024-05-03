from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserPydantic(BaseModel):
  pass


@app.get("/")
def index():
  return {"data":{"name":"Jacob"}}

@app.get("/about")
def about():
  return {"data":"data"}