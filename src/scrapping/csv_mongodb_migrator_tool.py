from indeed_mongodb_dao import IndeedMongodbDao
import json
import pandas as pd

class CsvToMongodbMigratorTool:
    def __init__(self):
        self.mongodbdao = IndeedMongodbDao()
        self.file_name = "../../data/indeed_mongo.csv"
    def migrate_to_mongo(self):
        dataset = pd.read_csv(self.file_name)
        records = json.loads(dataset.T.to_json()).values()
        self.mongodbdao.insert_data_bulk(records)

    def migrate_to_csv(self):
        data = self.mongodbdao.get_all_data()
        df = pd.DataFrame(list(data))
        df = df[~df.duplicated(subset=['description', 'adresse', 'titre'], keep='first')]
        df.to_csv(self.file_name)


#tool = CsvToMongodbMigratorTool()
#tool.migrate_to_csv()
