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
        self.collection_duplicate_data = self.db.duplicate_data
        
    def _valid_url_format(self,url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError as e:
            raise Exception('bad format for url {}'.format(url))
    
    def insert_data_bulk(self,data):
        try:
            self.collection.insert_many(data)
        except BulkWriteError as bwe:
            print(bwe.details)
            print(bwe.details['writeErrors'])
            raise
    
    
    def insert_to_dulicate_data(self,url):
        try:
            if url == "":
                raise Exception('url cannot be empty {}'.format(url))

            self._valid_url_format(url)

            line_to_insert = {"url": url}

            result = self.collection_duplicate_data.insert_one(line_to_insert) 
        except Exception as e:
            print(e)

    def _is_validate(self,url, title, name, description, localisation):
        error_message = ""
        if url == "":
                error_message = 'url cannot be empty {}'.format(url)

        self._valid_url_format(url)

        if title == "":
            error_message = 'title cannot be empty {}'.format(title)

        if name == "":
            error_message = 'the name of company cannot be be empty {}'.format(name)

        if description == "":
            error_message = 'description of company cannot be be empty {}'.format(description)

        if localisation == "":
            error_message = 'localisation of company cannot be be empty {}'.format(localisation)

        return error_message , len(error_message) > 0

    def update_data(self,id, url, title, name, address, publication_date, salary, description, contract_type):
        try:
            item_data = self.get_get_data_by_id(id)
            localisation = item_data["localisation"]
            error_message, error_state = self._is_validate(url,title, name, description, localisation)
            if error_state:
                raise Exception(error_message)

            line_to_update = {
                                "url": url,
                                "titre":title,
                                "nom_entreprise":name,
                                "adresse":address,
                                "date_de_publication":publication_date,
                                "salaire":salary,
                                "description":description,
                                "localisation":localisation,
                                "type_de_contrat":contract_type
                                }
            self.collection.update_one({'_id': id},{'$set': line_to_update}, upsert=False)
        except Exception as e:
            print(e)

    def insert_data(self, url, title, name, address, publication_date, salary, description, localisation, contract_type):
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
                                "salaire":salary,
                                "description":description,
                                "localisation":localisation,
                                "type_de_contrat":contract_type
                             }

            # Insert Data 
            result = self.collection.insert_one(line_to_insert) 
        except Exception as e:
            print(e)
    
    def get_all_data(self):
        data = self.collection.find({})
        return data

    def get_get_data_by_id(self, id):
        return self.collection.find({"_id" : id})[0]

    def description_exist(self, description):
        return self.collection.find({"description" : description}).count() > 0
        
    def url_exist(self, url):
        return self.collection.find({"url" : url}).count() > 0
    
    def url_exist_on_duplicate_data(self, url):
        return self.collection_duplicate_data.find({"url" : url}).count() > 0
    
    def get_all_duplicate(self):
        return self.collection.aggregate([{"$group" : { "_id": "$url", "count": { "$sum": 1 } }}, {"$match": {"_id" :{ "$ne" : None } , "count" : {"$gt": 1} } }, {"$project": {"u" : "$_id", "_id" : 0}}])
    
    def update_salary(self,id, salary):
        self.collection.update_one({'_id': id},{'$set': {'salaire': salary}}, upsert=False)
