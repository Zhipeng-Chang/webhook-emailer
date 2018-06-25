FROM python:3.6-stretch

WORKDIR /app
RUN pip install django
RUN pip install simplejson
RUN pip install django-tinymce
RUN pip install django mysqlclient
ADD webhook_emailer ./
ADD docker/entrypoint.sh /usr/local/bin/

CMD /bin/bash /usr/local/bin/entrypoint.sh