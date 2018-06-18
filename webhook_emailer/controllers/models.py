from django.db import models
from django.utils.translation import ugettext as _
from django.db import connections
from django.db.utils import OperationalError
from tinymce import models as tinymce_models
from django.core.validators import URLValidator

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
# python3 manage.py sqlmigrate controllers myNewMigration	
# python3 manage.py migrate

# Create your models here.
class NotificationTemplate(models.Model):
	NotificationTemplateText = tinymce_models.HTMLField()
	WebhookURL = models.URLField(null=False, blank=False)
	WebhookTitle = models.CharField(max_length=400)

class WebhookHistory(models.Model):
	WebhookName = models.URLField(null=False, blank=False, unique=True)
	WebhookID = models.IntegerField(unique=True)
	WebhookStatus = models.CharField(max_length=400)

class RequestValue(models.Model):
    
	status = models.CharField(
	    verbose_name = _(u'status'),
	    help_text = _(u'Submit, Review, Collaborate, Deliver '),
	    max_length = 255
	)
	ticketId = models.IntegerField(
	    verbose_name = _(u'ticketId'),
	    help_text = _(u' '),
	    default = -1
	)
	title = models.CharField(
	    verbose_name = _(u'title'),
	    help_text = _(u' '),
	    max_length = 255
	)
    
	ownerName = models.CharField(
	    verbose_name = _(u'ownerName'),
	    help_text = _(u' '),
	    max_length = 255
	)
    
	ownerEmail = models.CharField(
	    verbose_name = _(u'ownerEmail'),
	    help_text = _(u' '),
	    max_length = 255
	)
	    
	createdDate = models.CharField(
	    verbose_name = _(u'createdDate'),
	    help_text = _(u' '),
	    max_length = 255
	)
    
	description = models.CharField(
	    verbose_name = _(u'description'),
	    help_text = _(u' '),
	    max_length = 255
	)
    
	expectedTime = models.CharField(
	    verbose_name = _(u'expectśdTime'),
	    help_text = _(u' '),
	    max_length = 255
	) 
def __unicode__(self):
	return u'%s %s' % (self.repo_name, self.object_kind)