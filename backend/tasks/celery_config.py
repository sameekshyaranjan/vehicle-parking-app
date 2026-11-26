def configure_celery(app, celery_instance):
    """Configures a Celery instance with the Flask application context."""
    
 
    celery_instance.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery_instance.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    

    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask