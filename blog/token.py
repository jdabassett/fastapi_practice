from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
from typing import Dict

from . import schemas


# load environmental variables
load_dotenv()
# retrieve environmental variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# create new access token
def create_access_token(data: Dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'expire':expire.isoformat()})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_email_from_token(data, credentials_exception):
  try:
      payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload.get("sub")
      if email is None:
          raise credentials_exception
      token_data = schemas.TokenData(email=email)
  except JWTError:
      raise credentials_exception
  
  return token_data