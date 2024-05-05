from pydantic import BaseModel

class Blog(BaseModel):
  title: str
  body: str

class ShowBlog(BaseModel):
  id: int
  title:str
  class Config:
    orm_mode = True

class User(BaseModel):
  name:str
  email:str
  password:str

class ShowUser(BaseModel):
  id:int
  name:str
  class Config:
    orm_mode=True