from pymongo import  MongoClient
import pandas as pd
import json

conn = MongoClient()
dbnames = conn.list_database_names()
#if 'Indeed' not in dbnames:
db = conn.Indeed
collection_data = db.data
collection_duplicate_data = db.duplicate_data

df_data = pd.read_csv("../../data/indeed_mongo.csv")
data_records = json.loads(df_data.T.to_json()).values()
collection_data.insert_many(data_records)

df_duplicate_data = pd.read_csv("../../data/indeed_mongo_duplicate.csv")
data_duplicate_records = json.loads(df_duplicate_data.T.to_json()).values()
collection_duplicate_data.insert_many(data_duplicate_records)

print("data recorded in mongo database")
