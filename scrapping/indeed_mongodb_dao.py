from pymongo import MongoClient 
from pymongo import errors 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from pymongo.errors import BulkWriteError
class IndeedMongodbDao:
    def __init__(self):
        self.conn = MongoClient() 
        self.db = self.conn.Indeed
        self.collection = self.db.data
        
    def _valid_url_format(self,url):
        val = URLValidator()
        try:
            val(url)
        except:
            raise Exception('bad format for url {}'.format(url))
    
    def insert_data_bulk(self,data):
        try:
            self.collection.insert_many(data)
        except BulkWriteError as bwe:
            print(bwe.details)
            print(bwe.details['writeErrors'])
            raise
    
    def insert_data(self, url, title, name, address, publication_date,salaire, description, localisation):
        
        try:
            if url == "":
                raise Exception('url cannot be empty {}'.format(url))

            self._valid_url_format(url)

            if title == "":
                raise Exception('title cannot be empty {}'.format(title))

            if name == "":
                raise Exception('the name of company cannot be be empty {}'.format(title))

            if description == "":
                raise Exception('description of company cannot be be empty {}'.format(title))

            line_to_insert = {
                                "url": url,
                                "titre":title,
                                "nom_entreprise":name,
                                "adresse":address,
                                "date_de_publication":publication_date,
                                "salaire":salaire,
                                "description":description,
                                "localisation":localisation
                             }

            # Insert Data 
            self.collection.insert_one(line_to_insert) 
        except Exception as e:
            print(e)
    
    def get_all_data(self):
        data = self.collection.find({})
        return data
    
    def description_exist(self, description):
        return self.collection.find({"description" : description}).count() > 0
        
    def url_exist(self, url):
        return self.collection.find({"url" : url}).count() > 0
    
    def get_all_dupliate(self):
        return self.collection.aggregate([{"$group" : { "_id": "$url", "count": { "$sum": 1 } }}, {"$match": {"_id" :{ "$ne" : None } , "count" : {"$gt": 1} } }, {"$project": {"u" : "$_id", "_id" : 0}}])

    def update_salary(self,id, salaire):
        self.collection.update_one({'_id': id},{'$set': {'salaire': salaire}, upsert=False)