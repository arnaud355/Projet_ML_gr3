from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time

from datetime import datetime, timedelta
class IndeedPaser:
    def __init__(self):
        self.website = "https://www.indeed.fr"
        self.driverPath = "C:\\Users\\User\\Documents\\selenium\\driver\\chromedriver.exe"
        self.dao = IndeedMongodbDao()
        
        self.jobs = ["developpeur", "data scientist", "data analyst", "business intelligence"]
        self.locations = ["Lyon", "Toulouse", "Nantes", "Bordeaux","Paris"]
        self.indeed_item_parser = IndeedItemParser()
        self.keyWordsProvider = KeyWordsProvider()
    
    def _get_pages_counts(self,soup):
        searchCountPages = None
        try:
            #searchCountPages_elt = driver.find_element_by_id("searchCountPages")
            searchCountPages_elt = soup.select("#searchCountPages")
            if len(searchCountPages_elt) > 0:
                searchCountPages = searchCountPages_elt[0].text.strip().split()
        except Exception as e: 
            print(traceback.format_exc())
        
        if searchCountPages != None:    
            if len(searchCountPages) == 6:
                searchCountPages = int("{0}{1}".format(searchCountPages[3],searchCountPages[4])) 
            else :
                searchCountPages = searchCountPages[3] 
            result = (int(searchCountPages) // 18)

            if result == 1:
                result = 2
            return result
    
    def _get_subs_collections(self,items, nbr=5):
        result = []
        sub = []
        for index, item in enumerate(items):
            sub.append(item)
            if (index > 0) & (index % nbr) == 0:
                result.append(sub)
                sub = []
        return result
    
    def _local_parse_page(self, item_link,localisation):
        try:
            if self.dao.url_exist(item_link) == True:
                print("aready parsed, skip")
            elif self.dao.url_exist_on_duplicate_data(item_link) == True:
                print("duplicate url and aready parsed, skip")
            else:
                title, name, address, date,salaire, description = self.indeed_item_parser.parse(item_link)
                if self.dao.description_exist(description) == True:
                    self.dao.insert_to_dulicate_data(item_link)
                    print("duplicate. archived and skip.")
                    return
                if date == np.nan:
                    print("date nan - ", item_link)
                
                if (item_link != np.nan) & (title != np.nan) & (name != np.nan) & (address != np.nan) & (description != np.nan):
                    self.dao.insert_data(item_link,title,name,address,date,salaire,description,localisation)
                    print("saved :",item_link)   
                    print(salaire)
                
                #self.create_local_file(item_link, source)
        except Exception as e:
            print(traceback.format_exc())
    
    def randomString(self, stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
                    
    def create_local_file(self, item_link, source):
        file = open("pages/{0}.html".format(self.randomString()), "w")
        source = item_link + "----------------" + source
        file.write(source)
        file.close()
                    
    def parse(self):
        
        for job in self.jobs:
            jobs_filter_list = [job]
            
            if job == "developpeur":
                all_competences = self.keyWordsProvider.get_langages() + self.keyWordsProvider.get_tools() + self.keyWordsProvider.get_others()
                jobs_filter_list = ["{0} {1}".format(job, item) for item in all_competences]
            
            random.shuffle(jobs_filter_list)
            for job_key_word in jobs_filter_list:
                for location in self.locations:

                    query = recode_uri("https://www.indeed.fr/jobs?q={0}&l={1}".format(job_key_word, location))
                    print(query)
                    #browser.get(query)
                    page = request.urlopen(query)
                    soup = BeautifulSoup(page)
                    
                    pages_count = self._get_pages_counts(soup)
                    if pages_count == None:
                        print("No data on {0}, skip".format(query))
                        continue
                    
                    for page_index in random.sample(range(0, pages_count), pages_count):
                        full_query = recode_uri("{0}&start={1}".format(query,page_index))
                        #browser.get(full_query)
                        
                        item_page = request.urlopen(full_query)
                        item_soup = BeautifulSoup(item_page)
                        items = item_soup.select("a[class*='jobtitle']")
                        #items = browser.find_elements_by_xpath("//*[contains(@class,'clickcard')]//*[contains(@class,'jobtitle')]")
                        items = [urljoin(self.website, item["href"]) for item in  items]
                        
                        for index_i, link in enumerate(items):
                            self._local_parse_page(link, location)