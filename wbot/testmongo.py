from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['molipromotest']

users = db['users']

#users.insert_one({"_id": 12312312, "nombre": "alexander", "stage" : 1})

usuario = users.find_one({"_id": 12})

if usuario is None:
    print("sexoenlaplaya")

