from passlib.context import CryptContext

password_encryption = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
  def bcrypt(password:str):
    return password_encryption.hash(password)