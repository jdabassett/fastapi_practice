from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, hashing, models, schemas, token


router = APIRouter(
  tags=['Authentication']
)


# create route accept user credientials and return access token
@router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.email == form_data.username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
  if not hashing.Hash.verify(form_data.password, user.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
  
  access_token = token.create_access_token(data={"sub":user.email})
  
  return schemas.Token(access_token=access_token, token_type="Bearer")
  


