from flask import Flask
from celery import Celery


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads/original'
    app.config['PROCESSED_FOLDER'] = 'uploads/processed'
    
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERY_IMPORTS'] = ('app.tasks',)
    
    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    
    celery.conf.update({
        'imports': ('app.tasks',),
        'broker_url': app.config['CELERY_BROKER_URL'],
        'result_backend': app.config['CELERY_RESULT_BACKEND']
    })
    
    return celery