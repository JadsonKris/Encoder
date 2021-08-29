from sqlalchemy import Column, Integer, String
from .database import Base

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_input = Column(String)
    image_output = Column(String)
    ocr = Column(String)
