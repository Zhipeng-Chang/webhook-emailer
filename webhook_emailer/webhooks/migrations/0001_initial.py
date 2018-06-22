# Generated by Django 2.0.2 on 2018-06-22 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WebhookTitle', models.CharField(max_length=400)),
                ('NotificationTemplateText', tinymce.models.HTMLField()),
                ('RootURL', models.URLField()),
                ('WebhookURL', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('WebhookCreator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataIn', tinymce.models.HTMLField()),
                ('DataIn_date', models.DateField(auto_now_add=True, verbose_name='DataIn Date')),
                ('DataIn_time', models.TimeField(auto_now_add=True, verbose_name='DataIn Time')),
            ],
        ),
        migrations.CreateModel(
            name='WebhookHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WebhookName', models.URLField()),
                ('DataOut', tinymce.models.HTMLField()),
                ('WebhookStatus', models.CharField(max_length=400)),
                ('WebhookCreator', models.CharField(max_length=400)),
            ],
        ),
    ]
