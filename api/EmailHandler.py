import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHandler(object):
  def __init__(self, ConfigObj):
    self.ConfigObj = ConfigObj

  def send(self, email: str, subject: str, data: str) -> bool:
    try:
      # Create message object
      msg = MIMEMultipart()
      msg['From'] = self.ConfigObj.email_host_user
      msg['To'] = email
      msg['Subject'] = subject

      # Add message body
      msg.attach(MIMEText(data, 'plain'))

      # Create SMTP object
      server = smtplib.SMTP(self.ConfigObj.email_host, self.ConfigObj.email_port)

      # Login to email account
      server.starttls()
      server.login(self.ConfigObj.email_host_user, self.ConfigObj.email_host_password)

      # Send email
      server.sendmail(self.ConfigObj.email_host_user, email, msg.as_string())

      # Close SMTP connection
      server.quit()

      return True
    
    except Exception as e:
      print(e)
      return False