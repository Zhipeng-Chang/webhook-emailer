from django.db import models
from django.utils.translation import ugettext as _
from django.db import connections
from django.db.utils import OperationalError
db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    connected = False
else:
    connected = True

# When create a new model, run migration as follow:
# python manage.py makemigrations
# python manage.py sqlmigrate polls myNewMigration	
# python manage.py migrate

# Create your models here.
class NotificationTemplate(models.Model):
	NotificationTemplate_text = models.CharField(max_length=400)
	Webhook_id = models.IntegerField(default=0)

class Webhook(models.Model):
	Webhook_url = models.CharField(max_length=200)

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
	    verbose_name = _(u'expectedTime'),
	    help_text = _(u' '),
	    max_length = 255
	)

def __unicode__(self):
	return u'%s %s' % (self.repo_name, self.object_kind)