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

def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html',context={})

def myview(request):
    conn = connections['default']
    try:
        cursor = conn.cursor()
        cursor.execute("select status from controllers_RequestValue")
        rows = cursor.fetchall()
    finally:
        conn.close()

    return render(request,"", {"rows" : rows})

@csrf_exempt
<<<<<<< HEAD
def webhook_register(request):
    # Local variables 
    status = None
    ticketId = None
    title = None
    ownerName = None
    ownerEmail = None
    createdDate = None
    description = None
    expectedTime = None

=======
def gitlab_webhook_register(request):
>>>>>>> parent of cb4b6b2... update Docker file
    if request.method == 'POST' and request.body:
        initiative_data = json.loads(request.body)
        status = initiative_data.get('Status', '')
        ticketId = initiative_data.get('ID', '')
        title = initiative_data.get('Title', '')
        ownerName = initiative_data.get('OwnerName', '')
        ownerEmail = initiative_data.get('OwnerEmail', '')
        createdDate = initiative_data.get('CreatedDate', '')
        description = initiative_data.get('Description', '')
        expectedTime = initiative_data.get('ExpectedTime', '')

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
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Your Initiative has been updated'
        msg['From'] = gmail_user
        msg['To'] = ownerEmail
        statusTypeImage = ("https://octava.blob.core.windows.net/cdn-store/logoForEmailNotifications/process-%s-large.png"%(status.lower()))
        #Email body
        html = """\
        <html>
          <head></head>
        <p><img src="https://octava.blob.core.windows.net/cdn-store/logoForEmailNotifications/octava-banner-simple-large.png" alt="" width="600" height="31" /></p>
        <p><span style="font-family: 'times new roman', times; font-size: 12pt;">Hello {OwnerName},</span></p>
        <p><span style="font-size: 12pt; font-family: 'times new roman', times;">An OCT representative will be in contact with you about your request&nbsp;<strong>{ExpectedTime}</strong></span></p>
        <p>&nbsp;</p>
        <p><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>&nbsp;<img src={StatusTypeImage} alt="" width="448" height="51" /></strong></span></p>
        <p style="text-align: left;"><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>Request Number:</strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {ID}</span></p>
        <p style="text-align: left;"><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>Date &amp; Time:</strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{CreatedDate}</span></p>
        <p style="text-align: left;"><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>Status:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</strong><span style="color: #193a5a;">{Status}</span></span></p>
        <p style="text-align: left;"><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>User:</strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{OwnerName}</span></p>
        <p style="text-align: left;"><span style="font-size: 12pt; font-family: 'times new roman', times;"><strong>Description:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</strong>{Description}</span></p>
        <p>&nbsp;</p>
        <p><span style="font-size: 12pt; font-family: 'times new roman', times;">For further assistance please contact us on our Contact Page.</span></p>
        <p><span style="font-size: 12pt; font-family: 'times new roman', times;">Cheers,</span></p>
        <p><span style="font-size: 11pt; font-family: 'times new roman', times;"><span style="font-size: 12pt;">Open City and Technology</span> </span></p>
        </html>
        """.format(StatusTypeImage=statusTypeImage, OwnerName=ownerName, ExpectedTime=expectedTime, ID=ticketId, CreatedDate=createdDate, Status = status, Description=description )
        
        # Record the MIME types of both parts - text/plain and text/html.
        body = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(body)

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