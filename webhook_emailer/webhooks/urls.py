from django.urls import path
from . import views
# This two if you want to enable the Django Admin: (recommended)
from django.contrib import admin
from django.conf import settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.autodiscover()
urlpatterns =[
    path('', views.redrect_to_webhook_admin, name='redrect_to_webhook_admin'),
    path('util/webhook/url/<uuid:requestUrl>/', views.webhook_catch_octava, name='webhook-catch')

]
