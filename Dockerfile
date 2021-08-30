FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get -y install tesseract-ocr
RUN apt-get -y install default-libmysqlclient-dev
RUN pip3 install opencv-python==4.5.3.56
RUN pip3 install pydantic==1.8.2
RUN pip3 install Pillow==7.0.0
RUN pip3 install pytesseract==0.3.8
RUN pip3 install SQLAlchemy==1.4.23
RUN pip3 install tensorflow==2.6.0

COPY ./app /app
EXPOSE 8000
CMD ["python", "main.py"]
