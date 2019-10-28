from indeed_mongodb_dao import IndeedMongodbDao
import json
import pandas as pd

class CsvToMongodbMigratorTool:
    def __init__(self):
        self.mongodbdao = IndeedMongodbDao()
        self.file_name = "../../data/indeed_mongo.csv"
        self.file_name_duplicated = "../../data/indeed_mongo_duplicate.csv"

    def migrate_to_mongo(self):
        dataset = pd.read_csv(self.file_name)
        for col in dataset.columns:
            if "Unnamed" in col:
                dataset.drop(columns=[col], inplace=True)
        records = json.loads(dataset.T.to_json()).values()
        self.mongodbdao.insert_data_bulk(records)

        dataset_duplicated = pd.read_csv(self.file_name_duplicated)
        for col in dataset_duplicated.columns:
            if "Unnamed" in col:
                dataset_duplicated.drop(columns=[col], inplace=True)
        records_duplicated = json.loads(dataset_duplicated.T.to_json()).values()
        self.mongodbdao.insert_data_duplictaed_bulk(records_duplicated)




    def migrate_to_csv(self):
        data = self.mongodbdao.get_all_data()
        df = pd.DataFrame(list(data))
        df = df[~df.duplicated(subset=['description', 'adresse', 'titre'], keep='first')]
        df.to_csv(self.file_name)


#tool = CsvToMongodbMigratorTool()
#tool.migrate_to_mongo()
