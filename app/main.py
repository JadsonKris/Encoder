import uvicorn
from typing import List
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

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
    return crud.create_image(db=db, image=image)


@app.get("/image/", response_model=List[schemas.Image])
def get_images(db: Session = Depends(get_db)):
    return crud.get_images(db)


@app.get("/image/{id}", response_model=schemas.Image)
def get_image(id : int, db: Session = Depends(get_db)):
    return crud.get_image(db, image_id = id)


@app.delete("/image/{id}")
def delete_image(id: int, db: Session = Depends(get_db)) -> None:
    if not crud.delete_image(db, image_id = id):
        return {"error": "Image id:" + str(id) + "  not found"}
    else:
        return {"message", "image removed"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
