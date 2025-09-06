import os
from app.routes import app


if __name__ == '__main__':
    #Создание директоректорий при их отсутствии
    os.makedirs('uploads/original', exist_ok=True)
    os.makedirs('uploads/processed', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)