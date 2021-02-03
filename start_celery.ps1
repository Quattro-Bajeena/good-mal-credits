celery -A wsgi.celery worker --pool=solo -l INFO 
# celery -A wsgi.celery worker --pool=solo -l WARNING -f celery.log -l INFO 