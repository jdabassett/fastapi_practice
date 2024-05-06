from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=List[schemas.ShowBlog],
    
)
def all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).filter(models.Blog.user_id==current_user.id).all()
    return blogs


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.ShowBlog,
)
def show(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id == current_user.id).first()
    if not blog:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available"
        )
    return blog


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowBlog,
)
def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    current_user.blogs.append(new_blog)
    db.commit()
    return new_blog


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.ShowBlog,
)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id==current_user.id).first()
    if not updated_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    for attr, value in request.dict().items():
        setattr(updated_blog, attr, value)
    updated_blog.user_id = current_user.id
    db.commit()
    db.refresh(updated_blog)

    current_user.blogs.append(updated_blog)
    db.commit()

    return updated_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id==current_user.id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found.",
        )
    db.delete(blog)
    db.commit()
    return {"message": f"Record id {id} deleted."}
