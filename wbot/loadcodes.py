import csv

from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost'

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['molipromotest']
users = db['users']

db_codes = mongo_client['test_codes']
codes = db_codes['codes']
code_track = db_codes['track']

print("List of databases before deletion\n--------------------------")
for x in mongo_client.list_database_names():
  print(x)
  

mongo_client.drop_database('molipromotest')
mongo_client.drop_database('molipromo_codes')

print("\nList of databases after deletion\n--------------------------")
for x in mongo_client.list_database_names():
  print(x)



track = code_track.find_one({'_id':'counter'})


if track is None:
  code_track.insert_one({"_id": "counter", "count":0})
else:
  code_track.update_one({"_id": "counter"}, {"$set": { "count":0}})
  track = code_track.find_one({'_id':'counter'}) 
  print("counter reseted to", track['count'])


with open("./codes.csv", 'r') as file:
  csvreader = csv.reader(file)
  counter = 0
  for row in csvreader:
    cd = row[0]
    code = codes.find_one({"_id": counter})
    if code is not None:
        #print(code)
        codes.update_one({"_id": counter}, {"$set": { "used_by": ""}})
    if code is None:
        codes.insert_one({"_id": counter, "used_by": "", "code_id" : cd})
    counter += 1
