from celery import Celery

#tbh I have no idea where to put this function so it may as well be here

def make_celery(app, config_object):
    
    celery = Celery(app.import_name)
    celery.config_from_object(config_object)
    
    
    # for key in celery.conf:
    #     print(key, celery.conf[key])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# def celery_inspect(method):
#     app = Celery('app', broker='redis://')
#     inspect_result = getattr(app.control.inspect(), method)()
#     app.close()
#     return inspect_result
