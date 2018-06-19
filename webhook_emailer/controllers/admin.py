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
    #exclude = ('author',)
    list_display = ('WebhookTitle', 'RootURL', 'WebhookURL')
    list_filter = ('WebhookTitle', 'RootURL')
    search_fields = ('WebhookTitle', 'RootURL')
    readonly_fields=('WebhookURL','WebhookCreator')


    def has_change_permission(self, request, obj=None):
        has_class_permission = super(NotificationTemplateAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.WebhookCreator.id:
            return False
        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            return NotificationTemplate.objects.all()
        else:
            queryset = super(NotificationTemplateAdmin, self).get_queryset(request)
            return queryset.filter(WebhookCreator=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.WebhookCreator = request.user
        obj.save()

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
    search_fields = ('WebhookName', 'DataOut', 'WebhookStatus')
    readonly_fields= ('WebhookName', 'DataOut', 'WebhookStatus')
admin.site.register(WebhookHistory, WebhookHistoryAdmin)

