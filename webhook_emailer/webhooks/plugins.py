from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText    
from django.db import connections
from string import Formatter
import simplejson as json
import json

class UnseenFormatter(Formatter):
    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return ""
        else:
            return Formatter.get_value(key, args, kwds)

string = "{number_of_sheep} sheep {has} run away"
other_dict = {'number_of_sheep' : 1}

customed_format = UnseenFormatter()

def read_json_form_email(request, requestUrl, sent_from):
    requestValue = json.loads(request.body)
    requestUrlString = str(requestUrl).replace('-', '')
    #Send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your Initiative has been updated'
    msg['From'] = sent_from
    msg['To'] = requestValue.get('OwnerEmail', '')
    #Email body
    conn = connections['default']

    try:
        cursor = conn.cursor()
        cursor.execute("select NotificationTemplateText from webhooks_notificationtemplate where WebhookURL= \"%s\""%(requestUrlString))
        html_list = cursor.fetchall()
        cursor.execute("select WebhookTitle from webhooks_notificationtemplate where WebhookURL= \"%s\""%(requestUrlString))
        webhookTitle_list = cursor.fetchall()
        cursor.execute("select WebhookCreator_id from webhooks_notificationtemplate where WebhookURL= \"%s\""%(requestUrlString))
        webhookCreator_list = cursor.fetchall()
    finally:
        conn.close()

    try:
        html = html_list[0][0]
        webhookTitle = webhookTitle_list[0][0]
        webhookCreator = webhookCreator_list[0][0]
    except:
        raise EOFError ("Template ERROR")
    else:
        body = customed_format.format(html,**requestValue)

    # Record the MIME types of both parts - text/plain and text/html.
    emailbody = MIMEText(body, 'html') 
    msg.attach(emailbody)

    return msg.as_string(),webhookTitle, webhookCreator

