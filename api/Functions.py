import string, secrets, swiftcrypt, datetime, json
from typing import Dict, Tuple, Any
from django.http import HttpRequest

class Functions(object):
  def __init__(self, db, ConfigObj, LogHandlerObj):
    self.ConfigObj = ConfigObj
    self.db = db
    self.LogHandlerObj = LogHandlerObj
    
  def validateSigninData(self, email: str, password: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
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
        return({"errorCode":0, "errorMessage":"Success"}, account)
      return({"errorCode":1, "errorMessage":"Incorrect Password"}, account)
    return({"errorCode":1, "errorMessage":"No Account exists with that Email."}, {})

  def generateSessionId(self) -> str:
    """
    Generates a new Session ID for a User.

    Returns:
    str: A new Session ID for a User.
    """

    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    sessionId = ''.join(secrets.choice(characters) for i in range(self.ConfigObj.sessionId_length))
    return(sessionId)

  def validateAccountExistance(self, email: str) -> Dict[str, Any]:
    """
    Validates if an Account exists with the given Email.
    """

    if self.db.find_one("users", {"email":email}) == None:
      return({"errorCode":0, "errorMessage":"Success"})
    return({"errorCode":1, "errorMessage":"User already exists with this email"})

  def validateUsernameLimitations(self, username: str) -> Dict[str, Any]:
    """
    Validates the Username of a User.
    """

    if len(username) >= self.ConfigObj.username_min_length and len(username) <= self.ConfigObj.username_max_length and username.isalnum():
      return({"errorCode":0, "errorMessage":"Success"})
    return({"errorCode":1, "errorMessage":f"The username must have more than {self.ConfigObj.username_min_length} and less than {self.ConfigObj.username_max_length} characters"})

  def validatePasswordLimitations(self, password: str, rePassword: str) -> Dict[str, Any]:
    """
    Validates the Password of a User.
    """

    if password == rePassword and len(password) >= self.ConfigObj.password_min_length and len(password) <= self.ConfigObj.password_max_length:
      return({"errorCode":0, "errorMessage":"Success"})
    return({"errorCode":1, "errorMessage":f"The passwords must match and must have more than {self.ConfigObj.password_min_length} and less than {self.ConfigObj.password_max_length} characters"})

  def validateSignupData(self, email: str, username: str, password: str, rePassword: str) -> Dict[str, Any]:
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

    error = self.validateAccountExistance(email)
    if error["errorCode"] == 0:
      error = self.validateUsernameLimitations(username)
      if error["errorCode"] == 0:
        error = self.validatePasswordLimitations(password, rePassword)
        if error["errorCode"] == 0:
          pass
    return error


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

  def validateApiToken(self, token: Any) -> bool:
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
  
  def validateOtp(self, account: Dict[str, Any], otp: str) -> bool:
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
      
  def runCommonChecks(self, request: HttpRequest, endpoint: str, writeLogOnSuccess = False) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    """
    Runs the common checks for a request. The checks are the following:
    - Validate API Token
    - Validate Form
    - Validates Request Type to be POST
    """
    if request.method != "POST":
      self.LogHandlerObj.write(endpoint, "FAILED", {}, "", "Method not Allowed")
      return False, {}, {"errorCode":1, "errorMessage":"Method not Allowed."}
    else:
      try:
        data = json.loads(request.body)
        if self.validateApiToken(data.get("apiToken")):
          if writeLogOnSuccess:
            self.LogHandlerObj.write(endpoint, "OK", data, data["email"])
          return True, data, {"errorCode":0, "errorMessage":"Success"}
        return False, data, {"erorCode":1, "errorMessage":"Invalid API Token"}
      except Exception as e:
        print(e)
        self.LogHandlerObj.write(endpoint, "FAILED", data, "", "Invalid Form")
      return False, {}, {"errorCode":1, "errorMessage":"Invalid Form"}
    
  def runAllChecks(self, request: HttpRequest, endpoint: str) -> Tuple[bool, Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Runs all checks for a request. The checks other than the common ones are the following:
    - Validate API Token
    - Validate Session ID

    Args:
    request (HttpRequest): The Django Request Object.
    """
    success, data, error = self.runCommonChecks(request, endpoint)
    if success:
      if self.validateApiToken(data.get("apiToken")):
        account = self.db.find_one("users", {"email":data["email"]})
        if account != None:
          if self.validateSession(account, data):
            accountData = self.db.find_one("users-data", {"email":account["email"]})
            if accountData != None:
              self.LogHandlerObj.write(endpoint, "OK", data, data["email"])
              return True, data, account, accountData, {"errorCode":0, "errorMessage":"Success"}
            self.LogHandlerObj.write(endpoint, "FAILED", data, data["email"], "Error in Database")
            return False, data, account, accountData, {"errorCode":1, "errorMessage":"Error in Database"}
          self.LogHandlerObj.write(endpoint, "FAILED", data, data["email"], "Invalid Session ID")
          return False, data, account, {}, {"errorCode":1, "errorMessage":"Invalid Session ID"}
        self.LogHandlerObj.write(endpoint, "FAILED", data, data["email"], "No Account exists with that Email")
        return False, data, {}, {}, {"errorCode":1, "errorMessage":"No Account exists with that Email"}
      self.LogHandlerObj.write(endpoint, "FAILED", data, data["email"], "Invalid Api Token")
      return False, data, {}, {}, {"errorCode":1, "errorMessage":"Invalid Api Token"}
    else:
      return success, data, {}, {}, error
    
  def dPrint(self, message: str):
    if self.ConfigObj["debug"]:
      print(f"[DEBUG]: {message}")