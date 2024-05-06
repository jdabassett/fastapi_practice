from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import database, hashing, models, oauth2, schemas

router = APIRouter(
    prefix="/user",
    tags=['User']
    )

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_current_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).filter(models.User.id==current_user.id).all()
    return users

# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
# def get_user_by_id(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     user = db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find record of user id {id}.")
#     return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    try:
      hashed_password = hashing.Hash.bcrypt(request.password)
      new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{err}")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/", status_code=status.HTTP_201_CREATED)
def update_user(request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==current_user.id).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find record of user.")
    
    for attr, value in request.dict().items():
        if attr == "password":
            value = hashing.Hash.bcrypt(value)
        setattr(user, attr, value)
    db.commit()
    return {"message": "Record updated."}
    


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found.",
        )
    db.delete(user)
    db.commit()
    return {"message": "Record deleted."}
