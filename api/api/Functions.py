import string, secrets, swiftcrypt

class Functions(object):
  def __init__(self, db, ConfigObj):
    self.ConfigObj = ConfigObj
    self.db = db
    
  def validateSigninData(self, email, password):
    account = self.db.find_one("users", {"email":email})
    if account != None:
      if swiftcrypt.Checker().verify_password(password, account["passwordHash"], account["salt"], "sha256"):
        return(True, {"errorCode":0, "errorMessage":"Success"}, account)
      return(False, {"errorCode":1, "errorMessage":"Incorrect Password"}, account)
    return(False, {"errorCode":1, "errorMessage":"No Account exists with that Email."}, account)

  def generateSessionId(self):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    sessionId = ''.join(secrets.choice(characters) for i in range(self.ConfigObj.sessionId_length))
    return(sessionId)

  def validateSignupData(self, email, username, password, rePassword):
    if self.db.find_one("users", {"email":email}) == None:
      if len(username) >= self.ConfigObj.username_min_length and len(username) <= self.ConfigObj.username_max_length and username.isalnum():
        if password == rePassword and len(password) >= self.ConfigObj.password_min_length and len(password) <= self.ConfigObj.password_max_length:
          return(True, {"errorCode":0, "errorMessage":"Success"})
        return(False, {"errorCode":1, "errorMessage":f"The passwords must match and must have more than {self.ConfigObj.password_min_length} and less than {self.ConfigObj.password_max_length} characters"})
      return(False, {"errorCode":1, "errorMessage":f"The username must have more than {self.ConfigObj.username_min_length} and less than {self.ConfigObj.username_max_length} characters"})
    return(False, {"errorCode":1, "errorMessage":"User already exists with this email"})


  def validateSession(self, account, data):
    for entry in account["sessionIds"]:
      if entry["sessionId"] == data["sessionId"]:
        return(True)
    return(False)

  def validateApiToken(self, token):
    if token == False or token == None:
      return(False)
    elif self.db.find_one("api-tokens", {"apiToken":token}) != None:
      return(True)
    return(False)