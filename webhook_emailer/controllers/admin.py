from django.contrib import admin
from .models import NotificationTemplate
from .models import Webhook
from .models import RequestValue


# Register your models here.

admin.site.register(NotificationTemplate)
admin.site.register(Webhook)
admin.site.register(RequestValue)