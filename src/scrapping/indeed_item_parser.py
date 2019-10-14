from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time
import re
from multiprocessing import Pool
from functools import partial
from datetime import datetime, timedelta
import os.path
import os
from pymongo import MongoClient 
import pandas as pd 
import json
from pymongo import errors 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from pymongo.errors import BulkWriteError
from tempfile import NamedTemporaryFile
import string
import random
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
#from yelp_uri.encoding import recode_uri
import traceback

class IndeedItemParser:
    def __init__(self):
        self.driverPath = "C:\\Users\\User\\Documents\\selenium\\driver\\chromedriver.exe"
        self.salary_pattern = "[[S|s]alaire?[\s+]?:?[\s+]?(.*)e?[\s+]?\/(an|mois)|((.*)?[\s+]?par?[\s+]?(an|ans|mois|jour|heure))"
        
    def _get_title(self, soup):
        try:
            #title = driver.find_element_by_xpath("//*[@class='jobsearch-DesktopStickyContainer']//h3")
            title = soup.select(".jobsearch-DesktopStickyContainer h3")
            if len(title) > 0:
                return title[0].text
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
    
    def _get_name(self, soup):
        
        try:    
            #name = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[1]")
            name = soup.select("*[class*='jobsearch-InlineCompanyRating'] div")
            if len(name) > 0:
                return name[0].text
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
        
    
    def _get_address(self,soup):
         try:   
            #address = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[3]")
            address = soup.select("*[class*='jobsearch-InlineCompanyRating'] div")
            if address[2].text == "-":
                #address = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[4]")
                return address[3].text
            return address[2].text
         except Exception as e:
                #address = driver.find_element_by_xpath("//span[@class='jobsearch-JobMetadataHeader-iconLabel'][1]")
                address = soup.select("*[class*='jobsearch-JobMetadataHeader-iconLabel']")
                if len(address) > 0:
                    return address[0].text
                return np.nan
         
        
    def _get_salary_result(self,select_result):
        salary = np.nan
        for item in select_result:
            if "€" in item.text:
                outer_salary = re.compile(self.salary_pattern)
                m_salary = outer_salary.search(item.text)
                if m_salary is not None:
                    salary = m_salary.group(0)
                    break
        return salary

    def _get_salary(self,soup, url):
        try:
            #page = request.urlopen(url)
            #soup = BeautifulSoup(source)
            result = soup.select(".jobsearch-JobMetadataHeader-item")
            if len(result) > 0:
                return self._get_salary_result(result)

            result = soup.select(".jobsearch-JobMetadataHeader-itemWithIcon .jobsearch-JobMetadataHeader-iconLabel")
            if len(result) > 0:
                return self._get_salary_result(result)

            result = soup.select("#jobDescriptionText")
            if len(result) > 0:
                index = index + 1 
                outer_salary = re.compile(self.salary_pattern)
                m_salary = outer_salary.search(result[0].text)
                if m_salary is not None:
                    return self._get_salary_result(m_salary.group(0))
        
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
    
    def _get_description(self,soup):
        try:
            #jobDescriptionText
            #e_description = driver.find_element_by_id("jobDescriptionText")
            e_description = soup.select("#jobDescriptionText")
            if (len(e_description) > 0):
                return e_description[0].text
            return np.nan
        except Exception as e:
            print(traceback.format_exc())
    
    def _get_date(self,soup,url,name):
        #if name == np.nan:
        #    return np.nan
        try:
            #date_str = driver.find_element_by_xpath("//*[@class='jobsearch-JobMetadataFooter']")
            date = datetime.now()
            date_str = soup.select(".jobsearch-JobMetadataFooter")
            date_str_full = date_str[0].text.strip()
            
            re_pattern_count = re.compile(r"\s.*?(\d+\+)\s.*|\s.*?(\d+)\s.*")
            re_pattern_count = re_pattern_count.search(date_str_full)
            if re_pattern_count.group(2) != None:
                count = re_pattern_count.group(2).replace("+","")
            else: 
                count = re_pattern_count.group(1).replace("+","")
            
            if count == "30+":
                return date - timedelta(days=30)
            
            count = int(count)
            re_pattern_label = re.compile(r"\s.*?(jour|jours|heur|heurs|mois|an)")
            re_pattern_label = re_pattern_label.search(date_str_full)
            label = re_pattern_label.group(1)
            print("label -", label,"count -: ", count)
            
            if "jour" in label:
                date = date - timedelta(days=count)
            elif "heur" in label:
                date = date - timedelta(hours=count)
            return date;
        except Exception as e:
            print(traceback.format_exc())
    
    
    def parse(self,url):
        #driver = webdriver.Chrome(self.driverPath)
        #driver.get(url)
        #driver.maximize_window()
        print("page item ",url)
        page = request.urlopen(url)
        soup = BeautifulSoup(page)
        
        #source = driver.page_source
        title = self._get_title(soup)
        name = self._get_name(soup)
        if name == np.nan:
            print("name missing")
        address = self._get_address(soup)
        date = self._get_date(soup, url,name)
        description = self._get_description(soup)
        salaire = self._get_salary(soup,url)
        
        return title, name, address, date, salaire, description


