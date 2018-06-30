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
    readonly_fields=('RootURL','WebhookURL','WebhookCreator')


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
    list_display = ('DataIn', 'DataIn_date', 'DataIn_time')
    readonly_fields = ('DataIn', 'DataIn_date', 'DataIn_time')
    list_filter = ('DataIn_date', 'DataIn_time')
    search_fields = ('DataIn_date', 'DataIn_time')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(RequestValueAdmin, self).changeform_view(request, object_id, extra_context=extra_context)




    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        #Disable delete
        actions = super(RequestValueAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

admin.site.register(RequestValue, RequestValueAdmin)


class WebhookHistoryAdmin (admin.ModelAdmin):
    exclude=['WebhookCreator']
    list_display = ('WebhookName', 'WebhookStatus')
    list_filter = ('WebhookName', 'WebhookStatus')
    search_fields = ('WebhookName', 'DataOut', 'WebhookStatus')
    readonly_fields= ('WebhookName', 'DataOut', 'WebhookStatus')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(WebhookHistoryAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def has_add_permission(self, request):
        return False
        
    def get_actions(self, request):
        #Disable delete
        actions = super(WebhookHistoryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(WebhookHistoryAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.WebhookCreator.id:
            return False
        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            return WebhookHistory.objects.all()
        else:
            queryset = super(WebhookHistoryAdmin, self).get_queryset(request)
            return queryset.filter(WebhookCreator=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.WebhookCreator = request.user
        obj.save()
admin.site.register(WebhookHistory, WebhookHistoryAdmin)

