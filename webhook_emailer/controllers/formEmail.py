from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText        
def formAnEmail(sent_from, sent_to, status=None, ticketId=None, title=None, ownerName=None, ownerEmail=None, createdDate=None, description=None, expectedTime=None):
    #Send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your Initiative has been updated'
    msg['From'] = sent_from
    msg['To'] = sent_to
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
    msg.attach(body)

    return msg.as_string()
