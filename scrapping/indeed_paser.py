from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time

from datetime import datetime, timedelta
class indeedPaser:
    def __init__(self):
        self.website = "https://www.indeed.fr"
        self.driverPath = "C:\\Users\\Junior\\Documents\\selenium\\driver\\chromedriver.exe"
        self.dataset = pd.DataFrame(columns=['URL', 'Titre','Nom entreprise','Adresse','Date de publication', 'description'])
        self.jobs = ["développeur", "data scientist", "data analyst", "business intelligence"]
        self.locations = ["Paris", "Lyon", "Toulouse", "Nantes", "Bordeaux"]
        self.indeed_item_parser = IndeedItemParser()
        
    
    def parse(self):
        browser = webdriver.Chrome(self.driverPath)
        browser.get(self.website)
        browser.maximize_window()
        
        for job in self.jobs:
            for location in self.locations:
                query = "https://www.indeed.fr/jobs?q={0}&l={1}".format(job, location)
                browser.get(query)
        
                #searchCountPages
                searchCountPages_elt = browser.find_element_by_id("searchCountPages")
                searchCountPages = searchCountPages_elt.text.split()
                if len(searchCountPages) == 6:
                    searchCountPages = int("{0}{1}".format(searchCountPages[3],searchCountPages[4])) 
                else :
                    searchCountPages = searchCountPages[3]  
                    
                pages_count = (int)(searchCountPages / 18)
                
                for page_index in range(1, pages_count):
                    browser.get("{0}&start={1}".format(query,page_index))
                    
                    #jobsearch-SerpJobCard unifiedRow row result clickcard
                    items = browser.find_elements_by_xpath("//*[contains(@class,'clickcard')]")
                    dataset_len = len(self.dataset)
                    for index_i,item in enumerate(items): 
                        title = item.find_element_by_xpath(".//*[@class='title']//a")
                        item_link = title.get_attribute("href")
                        
                        if (len(self.dataset) == 0) | (item_link not in self.dataset["URL"]):
                            print("existe pas")
                            title, name, address, date, description = self.indeed_item_parser.parse(item_link)
                            self.dataset.loc[dataset_len + index_i] = [item_link, title, name, address, date,description]
                        else:
                            print("existe déjà")
                        
                        #break
                    #break
                    self.dataset.to_csv("indeed.csv", index=False)
                    #https://www.indeed.fr/jobs?q=developpeur&l=paris&start=10
                    
                print(searchCountPages)
                #break
            #break
           
                
                    
                    
                