from django.urls import path
from . import views
# This two if you want to enable the Django Admin: (recommended)
from django.contrib import admin
admin.autodiscover()


urlpatterns =[
	path('', views.index, name='index'),
    path('webhook/url/', views.gitlab_webhook_register, name='gitlab-webhook-register')

]
