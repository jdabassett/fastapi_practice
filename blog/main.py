from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import schemas
from .database import Base
from .models import Blog

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@app.get('/blog', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
  blogs = db.query(Blog).all()
  return blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id, response: Response, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id).first()
  if not blog:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
  return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id).delete(synchronize_session=False)
  db.commit()
  return {"message":"content deleted"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
  for attr, value in request.dict().items():
    setattr(blog, attr, value)
  db.commit()
  return {"message":f"Record id {id} updated."}

@app.put("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
  blog.delete(synchronize_session=False)
  db.commit()
  return {"message":f"Record id {id} deleted."}
