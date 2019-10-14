class CsvToMongodbMigratorTool:
    
    def __init__(self):
        self.dataset = pd.read_csv("indeed.csv")
        self.mongodbdao = IndeedMongodbDao()
        
    def migrate(self):
        records = json.loads(self.dataset.T.to_json()).values()
        self.mongodbdao.insert_data_bulk(records)
        