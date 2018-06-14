from django.contrib import admin
from .models import NotificationTemplate
from .models import Webhook
from .models import RequestValue
from django.db import models
from django.forms import TextInput, Textarea
from tinymce import models as tinymce_models


# Register your models here.

admin.site.register(Webhook)
admin.site.register(RequestValue)

admin.site.register(NotificationTemplate)