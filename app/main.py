import uvicorn
import tensorflow as tf
import numpy as np
from image_processor import ImageProcessor
from typing import List
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
import cv2 as cv2
from PIL import Image
import pytesseract


models.Base.metadata.create_all(bind=engine)
model = tf.keras.models.load_model('../model/model.h5')
image_processor = ImageProcessor()
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return {'message': 'This is encoder API!'}

@app.post("/image/", response_model=schemas.Image)
def create_image(image: schemas.ImageBase, db: Session = Depends(get_db)):
    img = image_processor.decoder(image.image_input)
    img = image_processor.pre_processing(img)

    img = img.reshape(-1, 172, 360, 1)
    img = tf.convert_to_tensor(img)
    img_final = model.predict(img)[0]

    img_final = img_final.reshape(258,540)
    img_final*=255

    new_p = Image.fromarray(img_final.astype(np.uint8))
    if new_p.mode != 'RGB':
        new_p = new_p.convert('RGB')
    ocr = pytesseract.image_to_string(new_p, lang='eng')
    ocr = ocr.split()
    ocr = " ".join(ocr)

    img_out64 = image_processor.encoder(img_final)
    new_image = schemas.ImageCreate(image_input=image.image_input,
                                    image_output=img_out64,
                                    ocr = ocr)
    #{"image_input": img_in64, "image_output":img_out64,
    #             "ocr":ocr}

    return crud.create_image(db, new_image)


@app.get("/image/", response_model=List[schemas.Image])
def get_images(db: Session = Depends(get_db)):
    return crud.get_images(db)


@app.get("/image/{id}", response_model=schemas.Image)
def get_image(id : int, db: Session = Depends(get_db)):
    return crud.get_image(db, image_id = id)


@app.delete("/image/{id}")
def delete_image(id: int, db: Session = Depends(get_db)):
    if not crud.delete_image(db, image_id = id):
        return {"error": "Image id:" + str(id) + "  not found"}
    else:
        return {"message": "image removed"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
