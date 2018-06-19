from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText    
from django.db import connections
import simplejson as json
import json



def formAnEmail(sent_from, sent_to, status=None, ticketId=None, title=None, ownerName=None, ownerEmail=None, createdDate=None, description=None, expectedTime=None):
    #Send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your Initiative has been updated'
    msg['From'] = sent_from
    msg['To'] = sent_to
    #Email body
    conn = connections['default']
    try:
        cursor = conn.cursor()
        cursor.execute("select NotificationTemplateText from controllers_notificationtemplate where WebhookTitle = \"%s\""%(status))
        html_list = cursor.fetchall()
    finally:
        conn.close()

    try:
        html = html_list[0][0]
    except:
        raise EOFError ("You don't have the template in your database")
    else:
        body = html.format(OwnerName=ownerName, ExpectedTime=expectedTime, ID=ticketId, CreatedDate=createdDate, Status = status, Description=description)

    # Record the MIME types of both parts - text/plain and text/html.
    emailbody = MIMEText(body, 'html') 
    msg.attach(emailbody)

    return msg.as_string()


def get_json_data(request):
    request_data = json.loads(request.body)
    format_str = " "
    for key, value in request_data.items() :
        single_value_tuple = [key,'=', '"' ,value,'"',', ']
        single_value = "".join(single_value_tuple)
        format_str+=single_value
    request_value_str = format_str.rstrip(", ")
    request_value_str.replace('"', ' ')