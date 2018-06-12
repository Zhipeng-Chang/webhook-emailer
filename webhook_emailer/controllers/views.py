from django.shortcuts import render
from django.template import loader
import simplejson as json
import smtplib
import json
import os
from .models import RequestValue
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

with open(os.path.join(os.path.dirname(__file__),"appsettings.json"), 'r') as EmailData:
    emailData = json.load(EmailData)
    gmail_user = emailData.get('Octave_Email', '')
    gmail_password = emailData.get('Octave_Email_Password', '')

def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html',context={})



@csrf_exempt
def gitlab_webhook_register(request):
    status = None
    ticketId = None
    title = None
    ownerName = None
    ownerEmail = None
    createdDate = None
    description = None
    expectedTime = None
    if request.method == 'POST' and request.body:
        json_data = json.loads(request.body)
        status = json_data.get('Status', '')
        ticketId = json_data.get('ID', '')
        title = json_data.get('Title', '')
        ownerName = json_data.get('OwnerName', '')
        ownerEmail = json_data.get('OwnerEmail', '')
        createdDate = json_data.get('CreatedDate', '')
        description = json_data.get('Description', '')
        expectedTime = json_data.get('ExpectedTime', '')
        print ("status: ",status)

        initiative_obj = RequestValue(status = status, ticketId = ticketId, title = title, ownerName = ownerName, ownerEmail = ownerEmail, createdDate = createdDate, description = description, expectedTime = expectedTime )
        initiative_obj.save()
        
        # Read the email password from different file 
        with open(os.path.join(os.path.dirname(__file__),"appsettings.json"), 'r') as EmailData:
            emailData = json.load(EmailData)
            gmail_user = emailData.get('Octave_Email', '')
            gmail_password = emailData.get('Octave_Email_Password', '')

        #Send email
        sent_from = gmail_user  
        to = [ownerEmail]
        msg = MIMEText((' Status: %s\n ID: %s\n Title: %s\n OwnerName: %s\n OwnerEmail: %s\n CreatedDate: %s\n Description: %s\n ExpectedTime: %s\n') % (status, ticketId, title, ownerName, ownerEmail, createdDate, description, expectedTime))
        msg['Subject'] = 'Your Initiative has been updated'
        msg['From'] = sent_from
        msg['To'] = ownerEmail

        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, msg.as_string())
            server.close()
        except:  
            print ('Something went wrong...')
        
        return HttpResponse('Successfully got the request!')

    else:
        return HttpResponse('Successfully got the request, but the json pattern doesnt match')