import smtplib, secrets, string, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OtpHandler(object):
  def __init__(self, ConfigObj, db):
    self.ConfigObj = ConfigObj
    self.db = db

  def validateOtp(self, email: str, otp: str) -> bool:
    try:
      # Getting account
      account = self.db.find_one("users", {"email":email})

      # Getting OTPs
      otps = account["otps"]

      # Checking if OTP is valid
      for otpData in otps:
        if otpData["otp"] == otp and datetime.datetime.strptime(otpData["expiry"], "%Y-%m-%d_%H:%M:%S") > datetime.datetime.now():
          return True

      return False
    except Exception as e:
      print(e)
      return False

  def sendOtp(self, email: str) -> bool:
    try:
      # Generate OTP
      otp = self.generateOtp()
      otpData = {
        "otp": otp,
        "expiry": (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime("%Y-%m-%d_%H:%M:%S")
      }

      # Create message object
      msg = MIMEMultipart()
      msg['From'] = self.ConfigObj.email_host_user
      msg['To'] = email
      msg['Subject'] = "APM OTP Verification"

      # Add message body
      msg.attach(MIMEText("Your OTP is: " + otp, 'plain'))

      # Create SMTP object
      server = smtplib.SMTP(self.ConfigObj.email_host, self.ConfigObj.email_port)

      # Login to email account
      server.starttls()
      server.login(self.ConfigObj.email_host_user, self.ConfigObj.email_host_password)

      # Send email
      server.sendmail(self.ConfigObj.email_host_user, email, msg.as_string())

      # Close SMTP connection
      server.quit()

      # Store OTP in database
      account = self.db.find_one("users", {"email": email})
      otps = account["otps"]
      otps.append(otpData)
      self.db.find_one_and_update("users", {"email": email}, "otps", otps)

      return True
    
    except Exception as e:
      print(e)
      return False


  def generateOtp(self):
    otp = ""
    for i in range(6):
      otp += secrets.choice(string.digits)
    return(otp)
