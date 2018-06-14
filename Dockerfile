FROM python:3.6-stretch

WORKDIR /app
ADD webhook_emailer ./
RUN pip install django
RUN pip install simplejson
RUN pip install  django-tinymce

RUN python -c "import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
   username='$Jackson', \
   email='$zhipeng.chang@edmonton.ca', \
   password='$jacksoncoe')"

CMD ["python", "manage.py", "loaddata", "load_template"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:9001"]