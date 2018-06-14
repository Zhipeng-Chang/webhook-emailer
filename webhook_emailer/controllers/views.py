import simplejson as json
import smtplib
import json
import os
from django.shortcuts import render
from django.template import loader
from .models import RequestValue
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db import connections
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import formEmail

def index(request):
    """
    View function for home page of site.
    """
    conn = connections['default']
    try:
        cursor = conn.cursor()
        cursor.execute("select NotificationTemplate_text from controllers_NotificationTemplate where Webhook_id == 1")
        rows = cursor.fetchall()
    finally:
        conn.close()
    print (rows)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html',context={"test": rows})

@csrf_exempt

def webhook_catch(request):
    if request.method == 'POST' and request.body.isvalid():
        initiative_data = json.loads(request.body)
        status = initiative_data.get('Status', '')
        ticketId = initiative_data.get('ID', '')
        title = initiative_data.get('Title', '')
        ownerName = initiative_data.get('OwnerName', '')
        ownerEmail = initiative_data.get('OwnerEmail', '')
        createdDate = initiative_data.get('CreatedDate', '')
        description = initiative_data.get('Description', '')
        expectedTime = initiative_data.get('ExpectedTime', '')
        
        # Save the initiative object to the database
        initiative_obj = RequestValue(status = status, ticketId = ticketId, title = title, ownerName = ownerName, ownerEmail = ownerEmail, createdDate = createdDate, description = description, expectedTime = expectedTime )
        initiative_obj.save()
        
        # Read the email password from different file 
        with open(os.path.join(os.path.dirname(__file__),"appsettings.json"), 'r') as EmailData:
            emailData = json.load(EmailData)
            gmail_user = emailData.get('Octave_Email', '')
            gmail_password = emailData.get('Octave_Email_Password', '')

        #Form the email body
        email = formEmail.formAnEmail(gmail_user, ownerEmail, status, ticketId, title, ownerName, ownerEmail, createdDate, description, expectedTime)
        
        # Log in to the email account
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, ownerEmail, email)
            server.close()
        except:  
            raise EOFError ('Unable to log in to the email account')
        
        return HttpResponse('Successfully got the request!')

    else:
        return HttpResponse('Successfully got the request, but the json pattern doesnt match')
