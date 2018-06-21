FROM python:3.6-stretch

WORKDIR /app
ADD webhook_emailer ./
ADD docker/entrypoint.sh /usr/local/bin/
RUN pip install django
RUN pip install simplejson
RUN pip install django-tinymce
RUN pip install django mysqlclient


CMD /bin/bash /usr/local/bin/entrypoint.sh