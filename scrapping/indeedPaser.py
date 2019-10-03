from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time

from datetime import datetime, timedelta
from datetime import datetime, timedelta
class IndeedPaser:
    def __init__(self):
        self.website = "https://www.indeed.fr"
        self.driverPath = "C:\\Users\\Junior\\Documents\\selenium\\driver\\chromedriver.exe"
        #self.dataset = pd.DataFrame(columns=['URL', 'Titre','Nom entreprise','Adresse','Date de publication', 'description'])
        self.dataset = pd.read_csv("indeed.csv")
        self.jobs = ["développeur", "data scientist", "data analyst", "business intelligence"]
        self.locations = ["Paris", "Lyon", "Toulouse", "Nantes", "Bordeaux"]
        self.utilities =  utilities()
        self.indeed_item_parser = IndeedItemParser()
        self.parser_state = IndeedParserStateHandler()
    
    def _get_pages_counts(self,driver):
        #searchCountPages
        searchCountPages_elt = driver.find_element_by_id("searchCountPages")
        searchCountPages = searchCountPages_elt.text.split()
        if len(searchCountPages) == 6:
            searchCountPages = int("{0}{1}".format(searchCountPages[3],searchCountPages[4])) 
        else :
            searchCountPages = searchCountPages[3]  
                    
        return (int)(searchCountPages / 18)
    
    def parse(self):
        browser = webdriver.Chrome(self.driverPath)
        browser.get(self.website)
        browser.maximize_window()
        
        for job in self.jobs:
            
            if self.parser_state.is_current_job(job) == False:
                continue
                    
            for location in self.locations:
                
                if self.parser_state.is_current_location(location) == False:
                    continue
                self.parser_state.save_state(job, location)
                
                query = "https://www.indeed.fr/jobs?q={0}&l={1}".format(job, location)
                browser.get(query)
                    
                pages_count = self._get_pages_counts(browser)
                
                for page_index in range(1, pages_count):
                    full_query = "{0}&start={1}".format(query,page_index)
                    
                    browser.get(full_query)
                    
                    items = browser.find_elements_by_xpath("//*[contains(@class,'clickcard')]")
                    dataset_len = len(self.dataset)
                    
                    for index_i,item in enumerate(items): 
                        title = item.find_element_by_xpath(".//*[contains(@class,'jobtitle')]")
                        item_link = title.get_attribute("href")
                        
                        if (len(self.dataset) == 0) | (item_link not in self.dataset["URL"]):
                            print("existe pas")
                            title, name, address, date, description = self.indeed_item_parser.parse(item_link)
                            self.dataset.loc[dataset_len + index_i] = [item_link, title, name, address, date,description]
                            print("len(dataset)", len(self.dataset))
                        else:
                            print("existe déjà")
                        
                        #break
                    #break
                    self.dataset.to_csv("indeed.csv", index=False)
                    #https://www.indeed.fr/jobs?q=developpeur&l=paris&start=10
                    
                print(searchCountPages)
                #break
            #break         