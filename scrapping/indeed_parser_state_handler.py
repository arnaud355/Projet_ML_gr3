import os.path
from os import path
import json

class IndeedParserStateObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)
        
class IndeedParserStateHandler:
    
    def __init__(self):
        self.filename = "indeed.parser.state.json"
        self.object = self._load_file()
        print(type(self.object))
        #self.object = IndeedParserStateObject(self.data)
    
    def save_state(self, job, location, page_request="", page_item_index=-1):
        self.object["job"] = job
        self.object["location"] = location
        self.object["page_request"] = page_request
        self.object["page_item_index"]  = page_item_index
        #self.data  = json.dumps(self.object)
        
        #data = json.dumps(self.object)
        self._save_file(self.object)
        #self.object = IndeedParserStateObject(self.data)
        
    def is_current_job(self, job):
        if (self.object["job"] == "") | (self.object["job"] == job):
            return True
        return False
    
    def is_current_location(self, location):
        if (self.object["location"] == "") | (self.object["location"] == location):
            return True
        return False
    
    def is_current_page_request(self, page_request):
        if (self.object["page_request"] == "") | (self.object["page_request"] == page_request):
            return True
        return False
    
    def _save_file(self, data):
         with open(self.filename, 'w') as outfile:
                json.dump(data, outfile)
                
    def _load_file(self):
        
        if path.exists(self.filename) == True:
            with open(self.filename) as json_file:
                data = json.load(json_file)
        else:
            data = {
                     "job": "",
                     "location":"",
                     "page_request":"",
                     "page_item_index":-1,
                    }
            with open(self.filename, 'w') as outfile:
                json.dump(data, outfile)
        
        return data
