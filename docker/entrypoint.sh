#!/bin/bash
if [ -f /etc/secrets/appsettings.json ]; then
  cp /etc/secrets/appsettings.json /app/controllers/
  echo "appsettings.json config specified."
else
  echo "No appsettings.json config specified."
fi

if [ -f /etc/secrets/settings.py ]; then
  cp /etc/secrets/settings.py /app/webhook_emailer/
  echo "settings.py specified."
else
  echo "No settings.py specified."
fi

python manage.py runserver 0.0.0.0:9001