FROM python:3.6-stretch

WORKDIR /app
ADD webhook_emailer ./
RUN pip install django
RUN pip install simplejson

CMD ["python", "manage.py", "runserver"]