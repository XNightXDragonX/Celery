import os
import uuid
from flask import request, jsonify, send_file
from app import create_app
from app.utils import allowed_file
from app.tasks import process_image_task


app = create_app()

@app.route('/upscale', methods=['POST'])
def upscale_image_route():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не обнаружен'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    if file and allowed_file(file.filename):
        # Генерация уникального имени файла
        file_id = str(uuid.uuid4())
        original_filename = f'{file_id}_original.{file.filename.rsplit('.', 1)[1].lower()}'
        processed_filename = f'{file_id}_processed.png'
        
        # Сохранение оригинального файла
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_path)
        
        #Запуск Сelery-задачи
        task = process_image_task.apply_async(args=[original_filename, processed_filename])
        
        return jsonify({'task_id': task.id}), 202
    
    return jsonify({'error': 'Недопустимый формат файла'}), 400


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = process_image_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'status': 'В обработке'
        }
    elif task.state == 'SUCCESS':
        result = task.result
        response = {
            'status': result['status'],
            'processed_file': result.get('processed_file')
        }
    else:
        response = {
            'status': task.state
        }
        
    return jsonify(response)


@app.route('/processed/<filename>', methods=['GET'])
def get_processed_file(filename):
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    
    if not os.path.exists(processed_path):
        return jsonify({'error': 'Файл не найден'}), 404
    
    return send_file(processed_path, mimetype='image/png')