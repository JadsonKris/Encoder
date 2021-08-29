from typing import List, Optional

from pydantic import BaseModel


class ImageBase(BaseModel):
    image_input: str
    image_output: str
    ocr: str


class Image(ImageBase):
    id: int
    class Config:
        orm_mode = True
