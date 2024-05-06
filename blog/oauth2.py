from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from . import database, models, token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# validates that token is authentic and returns user
def get_current_user(data: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = token.get_email_from_token(data, credentials_exception)
    user = db.query(models.User).filter(models.User.email==token_data.email).first()
    if user is None:
        raise credentials_exception
    return user