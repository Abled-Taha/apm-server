import sys

# Non-Argument function
def setupConfig():
    from api.Config import Config as ConfigClass
    
    # Setting up Config
    global ConfigObj
    BASE_DIR = "./api"
    ConfigObj = ConfigClass(BASE_DIR)
    ConfigObj.readConfig()
  
def setupDatabase():
    from api.DatabaseHandler import DatabaseHandler as DatabaseHandlerClass
    
    setupConfig()
    
    # Setting up Database
    global db
    db = DatabaseHandlerClass(ConfigObj.db_name, ConfigObj.db_host, ConfigObj.db_port, ConfigObj.db_username, ConfigObj.db_password, ConfigObj.db_srv)
  
  

# Argument function
def run_server():
    import os, subprocess

    # Running wsgi server
    setupConfig()
    
    os.chdir("./api")
    try:
      subprocess.call(["waitress-serve", f"--listen={ConfigObj.server_host}:{ConfigObj.server_port}", "api.wsgi:application"])
    except:
      print("Stopped.")

def generate_api_token():
    import string, secrets
    
    # Taking API Token name as Input
    name = input("Enter API Token Name: ")
    
    # Code to generate API goes here
    setupDatabase()
    
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    apiToken = ''.join(secrets.choice(characters) for i in range(20))
    
    print(f"API Token: {apiToken}")
    print(f"API Token Name: {name}")
    
    # Asking if to save to db
    save = input("Save to Database? (y/n): ")
    if save == "y":
      db.insert_one("api-tokens", {"name":name, "apiToken":apiToken})
      print("Saved to Database")
      
def help():
  print("Use run-server flag to run the server")
  print("Use generate-api-token flag to generate API Token")
  print("Use help flag to get help")



if __name__ == "__main__":
    try:
      if sys.argv[1] == "run-server":
        run_server()
      elif sys.argv[1] == "generate-api-token":
        generate_api_token()
      else:
        help()
    except Exception as e:
      print(e)
      print("Provide a valid argument")
      print("Use help for more information")