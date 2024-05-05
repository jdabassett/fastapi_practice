from sqlalchemy import Boolean, String, Column, Integer
from sqlalchemy.orm import relationship

from .database import Base

class Blog(Base):
  __tablename__ = "blog"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  body = Column(String)