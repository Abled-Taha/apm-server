import pymongo

def connect(hostDB, portDB, nameDB, username, pwd):
  client = pymongo.MongoClient(f"mongodb://{username}:{pwd}@{hostDB}:{portDB}/?authSource={nameDB}")
  db = client[f"{nameDB}"]
  colUsers = db["users"]
  colUsersData = db["users-data"]

  return(client, db, colUsers, colUsersData)