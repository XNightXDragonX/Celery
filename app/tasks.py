import os
from celery import current_app
from app.utils import upscale_image


@current_app.task
def process_image_task(original_filename, processed_filename):
    """
    Celery-задача для обработки изображения
    """
    try:
        input_path = os.path.join('uploads/original', original_filename)
        output_path = os.path.join('uploads/processed', processed_filename)
        
        upscale_image(input_path, output_path)
        
        return {
            'status': 'Выполнено',
            'processed_file': processed_filename
        }
    except Exception as e:
        return {
            'status': 'Не удалось выполнить',
            'error': str(e)
        }