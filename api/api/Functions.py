import string, secrets, swiftcrypt, datetime
from typing import Dict, Tuple, Any

class Functions(object):
  def __init__(self, db, ConfigObj):
    self.ConfigObj = ConfigObj
    self.db = db
    
  def validateSigninData(self, email: str, password: str) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    """
    Validates the Signin Data of a User.

    Args:
    email (str): The Email of the User.
    password (str): The Password of the User.

    Returns:
    Tuple[bool, Dict[str, Any], Dict[str, Any]]: A tuple containing a boolean indicating if the signin was valid, a dictionary containing an errorCode and errorMessage, and a dictionary containing the User's data.
    """

    account = self.db.find_one("users", {"email":email})
    if account != None:
      if swiftcrypt.Checker().verify_password(password, account["passwordHash"], account["salt"], "sha256"):
        return(True, {"errorCode":0, "errorMessage":"Success"}, account)
      return(False, {"errorCode":1, "errorMessage":"Incorrect Password"}, account)
    return(False, {"errorCode":1, "errorMessage":"No Account exists with that Email."}, account)

  def generateSessionId(self) -> str:
    """
    Generates a new Session ID for a User.

    Returns:
    str: A new Session ID for a User.
    """

    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    sessionId = ''.join(secrets.choice(characters) for i in range(self.ConfigObj.sessionId_length))
    return(sessionId)

  def validateSignupData(self, email: str, username: str, password: str, rePassword: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates the Signup Data of a User.

    Args:
    email (str): The Email of the User.
    username (str): The Username of the User.
    password (str): The Password of the User.
    rePassword (str): The Re-Password of the User.

    Returns:
    Tuple[bool, Dict[str, Any]]: A tuple containing a boolean indicating if the signup was valid, and a dictionary containing an errorCode and errorMessage.
    """

    if self.db.find_one("users", {"email":email}) == None:
      if len(username) >= self.ConfigObj.username_min_length and len(username) <= self.ConfigObj.username_max_length and username.isalnum():
        if password == rePassword and len(password) >= self.ConfigObj.password_min_length and len(password) <= self.ConfigObj.password_max_length:
          return(True, {"errorCode":0, "errorMessage":"Success"})
        return(False, {"errorCode":1, "errorMessage":f"The passwords must match and must have more than {self.ConfigObj.password_min_length} and less than {self.ConfigObj.password_max_length} characters"})
      return(False, {"errorCode":1, "errorMessage":f"The username must have more than {self.ConfigObj.username_min_length} and less than {self.ConfigObj.username_max_length} characters"})
    return(False, {"errorCode":1, "errorMessage":"User already exists with this email"})


  def validateSession(self, account: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """
    Validates the Session ID of a User.

    Args:
    account (Dict[str, Any]): The User's data.
    data (Dict[str, Any]): The data containing the Session ID to validate.

    Returns:
    bool: True if the Session ID is valid, False otherwise.
    """

    for entry in account["sessionIds"]:
      if entry["sessionId"] == data["sessionId"]:
        return(True)
    return(False)

  def validateApiToken(self, token: str) -> bool:
    """
    Validates the API Token of a User.

    Args:
    token (str): The API Token to validate.

    Returns:
    bool: True if the API Token is valid, False otherwise.
    """

    if token == False or token == None:
      return(False)
    elif self.db.find_one("api-tokens", {"apiToken":token}) != None:
      return(True)
    return(False)
  
  def generateOtp(self):
    """
    Generates a new OTP (One Time Password) for a User.

    Returns:
    str: A new OTP for a User.
    """

    otp = ""
    for i in range(6):
      otp += secrets.choice(string.digits)
    return(otp)
  
  def validateOtp(self, account: Dict[str, Any], email: str, otp: str) -> bool:
    """
    Validates the OTP (One Time Password) of a User.

    Args:
    account (Dict[str, Any]): The account of the User.
    email (str): The Email of the User.
    otp (str): The OTP to validate.

    Returns:
    bool: True if the OTP is valid, False otherwise.
    """

    try:
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