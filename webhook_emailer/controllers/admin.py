from django.contrib import admin
from .models import NotificationTemplate
from .models import WebhookHistory
from .models import RequestValue
from django.db import models
from django.forms import TextInput, Textarea
from tinymce import models as tinymce_models


# Register your models here.


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
    list_display = ('title', 'status', 'createdDate','ticketId','ownerName')
    readonly_fields = ('title', 'status', 'createdDate','ticketId','ownerName', 'ownerEmail',  'description', 'expectedTime')
    list_filter = ('status', 'title', 'ownerName', 'ownerEmail')
    search_fields = ('status', 'ticketId', 'title', 'ownerName', 'ownerEmail', 'createdDate', 'description')

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(RequestValue, RequestValueAdmin)


class WebhookHistoryAdmin (admin.ModelAdmin):
    list_display = ('WebhookName', 'DataOut', 'WebhookStatus')
    list_filter = ('WebhookName', 'WebhookStatus')
    search_fields = ('WebhookName','WebhookStatus')
    readonly_fields= ('WebhookName', 'DataOut', 'WebhookStatus')
admin.site.register(WebhookHistory, WebhookHistoryAdmin)

