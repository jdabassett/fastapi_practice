from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, SessionLocal
from .hashing import Hash
from .models import Blog, User
from . import schemas

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available"
        )
    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    for attr, value in request.dict().items():
        setattr(blog, attr, value)
    db.commit()
    return {"message": f"Record id {id} updated."}


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    db.delete(blog)
    db.commit()
    return {"message": f"Record id {id} deleted."}


@app.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['user'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['user'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find record of user id {id}.")
    return user
    


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db), tags=['user']):
    try:
      hashed_password = Hash.bcrypt(request.password)
      new_user = User(name=request.name, email=request.email, password=hashed_password)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{err}")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/user/{id}", status_code=status.HTTP_201_CREATED, tags=['user'])
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find record of user id {id}.")
    
    for attr, value in request.dict().items():
        if attr == "password":
            value = Hash.bcrypt(value)
        setattr(user, attr, value)
    db.commit()
    return {"message": f"Record id {id} updated."}
    


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found.",
        )
    db.delete(user)
    db.commit()
    return {"message": f"Record id {id} deleted."}
