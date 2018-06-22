from django.db import models
from django.utils.translation import ugettext as _
from django.db import connections
from django.db.utils import OperationalError
from tinymce import models as tinymce_models
from django.core.validators import URLValidator
import uuid
from django.contrib.auth.models import User



field = models.TextField(validators=[URLValidator()])
db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    connected = False
else:
    connected = True

# When create a new model, run migration as follow:
# python3 manage.py makemigrations
# python3 manage.py sqlmigrate webhooks myNewMigration	
# python3 manage.py migrate

# Create your models here.
class NotificationTemplate(models.Model):
    WebhookTitle = models.CharField(max_length=400)
    NotificationTemplateText = tinymce_models.HTMLField()
    RootURL = models.URLField(null=False, blank=False)
    WebhookURL = models.UUIDField(default=uuid.uuid4, editable=False)
    WebhookCreator = models.ForeignKey(User,related_name='entries', on_delete=models.PROTECT)

class WebhookHistory(models.Model):
    WebhookName = models.URLField(null=False, blank=False)
    DataOut = tinymce_models.HTMLField()
    WebhookStatus = models.CharField(max_length=400)
    WebhookCreator = models.CharField(max_length=400)

class RequestValue(models.Model):
    DataIn = tinymce_models.HTMLField()
    DataIn_date = models.DateField(_(u"DataIn Date"), auto_now_add=True, blank=True)
    DataIn_time = models.TimeField(_(u"DataIn Time"), auto_now_add=True, blank=True)

    
def __unicode__(self):
	return u'%s %s' % (self.repo_name, self.object_kind)