FROM python:3.6-stretch

WORKDIR /app
RUN pip install django
RUN pip install simplejson
ADD webhook_emailer ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:9001"]