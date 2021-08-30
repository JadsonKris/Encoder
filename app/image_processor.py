import numpy as np
import cv2 as cv2
import base64
from PIL import Image
from io import BytesIO


class ImageProcessor(object):
    def decoder(self, string64):
        img = Image.open(BytesIO(base64.b64decode(string64)))
        img = np.array(img)
        return img

    def encoder(self, image):
        retval, buffer = cv2.imencode('.png', image)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text

    def pre_processing(self, image):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        img = cv2.GaussianBlur(image, (3,3), 0)
        img = cv2.Laplacian(img, cv2.CV_8U)
        img = np.invert(img)

        thresh = 230
        super_threshold_indices = img > thresh
        img[super_threshold_indices] =  254
        low_threshold_indices = img < thresh
        img[low_threshold_indices] =  0

        img = cv2.resize(img, (360 , 172) , interpolation=cv2.INTER_CUBIC)

        return img/255
