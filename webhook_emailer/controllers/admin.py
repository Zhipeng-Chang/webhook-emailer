from django.contrib import admin
from .models import NotificationTemplate
from .models import WebhookHistory
from .models import RequestValue
from django.db import models
from django.forms import TextInput, Textarea
from tinymce import models as tinymce_models


# Register your models here.

admin.site.register(WebhookHistory)

class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message',
        ''
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class NotificationTemplateAdmin (admin.ModelAdmin):
    list_display = ('WebhookTitle', 'RootURL', 'WebhookURL')
    list_filter = ('WebhookTitle', 'RootURL')
    search_fields = ('WebhookTitle', 'RootURL')
    readonly_fields=('WebhookURL',)

admin.site.register(NotificationTemplate, NotificationTemplateAdmin)

class RequestValueAdmin (admin.ModelAdmin):
    list_display = ('createdDate','ticketId','ownerName', 'status', 'title')
    list_filter = ('status', 'title', 'ownerName', 'ownerEmail')
    search_fields = ('status', 'ticketId', 'title', 'ownerName', 'ownerEmail', 'createdDate', 'description')

admin.site.register(RequestValue, RequestValueAdmin)

