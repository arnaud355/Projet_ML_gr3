from pymongo import MongoClient 
from pymongo import errors 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
class IndeedMongodbDao:
    def __init__(self):
        self.conn = MongoClient() 
        self.db = self.conn.Indeed
        self.collection = self.db.data
        self._create_index()
    
    def _create_index(self):
        index_name = 'url'
        if index_name not in self.collection.index_information():
            self.collection.create_index(index_name, unique=True)
    
    def _valid_url_format(self,url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError as e:
            raise Exception('bad format for url {}'.format(ur))
    
    def insert_data_bulk(self,data):
        self.collection.insert_many(data)
    
    def insert_data(self, url, title, name, address, publication_date, description):
        
        try:
            if url == "":
                raise Exception('url cannot be empty {}'.format(ur))

            self._valid_url_format(url)

            if title == "":
                raise Exception('title cannot be empty {}'.format(title))

            if name == "":
                raise Exception('the name of company cannot be be empty {}'.format(title))

            if description == "":
                raise Exception('description of company cannot be be empty {}'.format(title))


            line_to_insert = {
                                "URL": url,
                                "title":title,
                                "name":name,
                                "adresse":address,
                                "publication_date":publication_date,
                                "description":description
                             }

            # Insert Data 
            result = self.collection.insert_one(line_to_insert) 
        except errors.DuplicateKeyError as e:
            print('DuplicateKeyError : url {0} aready exist'.format(url))
    
    def get_all_data(self):
        data = self.collection.find({})
        return data
    
    