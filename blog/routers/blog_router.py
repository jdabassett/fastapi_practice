from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=List[schemas.ShowBlog],
)
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.ShowBlog,
)
def show(id: int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available"
        )
    return blog


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=schemas.ShowBlog,
)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=schemas.ShowBlog,
)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    for attr, value in request.dict().items():
        setattr(blog, attr, value)
    db.commit()
    return {"message": f"Record id {id} updated."}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    db.delete(blog)
    db.commit()
    return {"message": f"Record id {id} deleted."}
