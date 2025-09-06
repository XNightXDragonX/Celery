import os
import uuid
import cv2
from cv2 import dnn_superres


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp'}


def upscale_image(input_path: str, output_path: str, model_path: str = 'app/models/EDSR_x2.pb') -> None:
    """
    Функция для апскейлинга изображений
    """
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel('edsr', 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)