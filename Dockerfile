FROM python:3.6-stretch

WORKDIR /app
ADD webhook_emailer ./
RUN pip install django
RUN pip install simplejson
RUN pip install  django-tinymce

CMD ["python", "manage.py", "loaddata", "load_template"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:9001"]