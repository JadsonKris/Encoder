from sqlalchemy.orm import Session
from . import models, schemas


def get_images(db: Session):
    query = db.query(models.Image).all()
    return query


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def delete_image(db: Session, image_id: int):
    if image := get_image(db, image_id):
        db.delete(image)
        db.commit()
        return True

    return False


def create_image(db: Session, image: schemas.ImageCreate):
    new_image = models.Image(image_input=image.image_input,
                          image_output=image.image_output,
                          ocr = image.ocr)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image
