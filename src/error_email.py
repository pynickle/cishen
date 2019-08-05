import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
sender = '2330458484@qq.com'
receivers = ['code_nick_python@yeah.net']
 
mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP("smtp.yeah.net")
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except Exception as e:
    print(e)