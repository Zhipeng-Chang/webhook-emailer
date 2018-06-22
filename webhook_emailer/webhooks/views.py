import simplejson as json
import smtplib
import json
import os
from django.shortcuts import render
from django.template import loader
from .models import RequestValue
from .models import WebhookHistory
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db import connections
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import plugins

@csrf_exempt
def webhook_catch_octava(request,requestUrl):
    if request.method == 'POST' and request.body:
        # Save the request object to the database as datain history
        request_data = json.loads(request.body)
        request_obj = RequestValue(DataIn = request_data)
        request_obj.save()
        
        # Read the email password from different file 
        with open(os.path.join(os.path.dirname(__file__),"appsettings.json"), 'r') as EmailData:
            emailData = json.load(EmailData)
            gmail_user = emailData.get('Octave_Email', '')
            gmail_password = emailData.get('Octave_Email_Password', '')

        #Form the email body
        email,webhookName,webhookCreator = plugins.read_json_form_email(request, requestUrl, gmail_user)
        # Log in to the email account
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            send_to = request_data.get('OwnerEmail', '')
            server.sendmail(gmail_user, send_to, email)
            server.close()
            webhookHistory_obj = WebhookHistory(WebhookName = webhookName, DataOut = email, WebhookStatus = 'Success!', WebhookCreator =webhookCreator)
            webhookHistory_obj.save()
        except:  
            webhookHistory_obj = WebhookHistory(WebhookName = requestUrl, DataOut = email, WebhookStatus = 'Failed! Email ERROR.',WebhookCreator =webhookCreator)
            webhookHistory_obj.save()
            raise EOFError ('Email ERROR')
        return HttpResponse('Successfully got the request!')

    else:
        return HttpResponse('Successfully got the request, but the json pattern doesnt match')
    

def redrect_to_webhook_admin(request):
    return HttpResponseRedirect("util/webhook/")