from typing import List, Optional

from pydantic import BaseModel


class ImageBase(BaseModel):
    image_input: str


class ImageCreate(BaseModel):
    image_input: str
    image_output: str
    ocr: str


class Image(ImageCreate):
    id: int
    class Config:
        orm_mode = True
