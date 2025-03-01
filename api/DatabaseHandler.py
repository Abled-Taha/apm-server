import pymongo

class DatabaseHandler(object):
  def __init__(self, db_name, db_host, db_port, db_username, db_password, db_srv):
    if db_srv == False:
      self.client = pymongo.MongoClient(f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/?authSource={db_name}")
    else:
      self.client = pymongo.MongoClient(f"mongodb+srv://{db_username}:{db_password}@{db_host}")
    self.db = self.client[f"{db_name}"]
    self.collectionUsers = self.db["users"]
    self.collectionUsersData = self.db["users-data"]
    self.collectionAdminUsers = self.db["admin-users"]
    self.collectionApiTokens = self.db["api-tokens"]
    
  def find_one(self, collection, query):
    if collection == "users":
      result = self.collectionUsers.find_one(query)
      return(result)
    elif collection == "users-data":
      result = self.collectionUsersData.find_one(query)
      return(result)
    elif collection == "admin-users":
      result = self.collectionAdminUsers.find_one(query)
      return(result)
    elif collection == "api-tokens":
      result = self.collectionApiTokens.find_one(query)
      return(result)
    return(None)
  
  def insert_one(self, collection, data):
    if collection == "users":
      self.collectionUsers.insert_one(data)
      return(True)
    elif collection == "users-data":
      self.collectionUsersData.insert_one(data)
      return(True)
    elif collection == "admin-users":
      self.collectionAdminUsers.insert_one(data)
      return(True)
    elif collection == "api-tokens":
      self.collectionApiTokens.insert_one(data)
      return(True)
    return(None)
  
  def find_one_and_update(self, collection, query, fieldName, fieldData):
    if collection == "users":
      result = self.collectionUsers.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    elif collection == "users-data":
      result = self.collectionUsersData.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    elif collection == "admin-users":
      result = self.collectionAdminUsers.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    elif collection == "api-tokens":
      result = self.collectionApiTokens.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    return(None)