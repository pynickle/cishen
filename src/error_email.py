import smtplib
from email.mime.text import MIMEText
from email.header import Header

def mail(exception):
    sender = '2330458484@qq.com'
    receivers = ['2330458484@qq.com']
    
    msg = ""
    msg += "<p>Exception happened when others using your cishen application:</p>"
    msg += "<pre><code>" + exception + "</code></pre>"

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("cishen", 'utf-8')
    message['To'] =  Header("pynickle", 'utf-8')
    
    subject = 'cishen error occured'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP("smtp.yeah.net")
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except Exception as e:
        return False