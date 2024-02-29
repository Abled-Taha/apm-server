import pymongo

class DatabaseHandler(object):
  def __init__(self, db_name, db_host, db_port, db_username, db_password):
    self.client = pymongo.MongoClient(f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/?authSource={db_name}")
    self.db = self.client[f"{db_name}"]
    self.collectionUsers = self.db["users"]
    self.collectionUsersData = self.db["users-data"]
    
  def find_one(self, collection, query):
    if collection == "users":
      result = self.collectionUsers.find_one(query)
      return(result)
    elif collection == "users-data":
      result = self.collectionUsersData.find_one(query)
      return(result)
    return(None)
  
  def insert_one(self, collection, data):
    if collection == "users":
      self.collectionUsers.insert_one(data)
      return(True)
    elif collection == "users-data":
      self.collectionUsersData.insert_one(data)
      return(True)
    return(None)
  
  def find_one_and_update(self, collection, query, fieldName, fieldData):
    if collection == "users":
      result = self.collectionUsers.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    elif collection == "users-data":
      result = self.collectionUsersData.find_one_and_update(query, {"$set":{fieldName:fieldData}})
      return(result)
    return(None)