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
            title = soup.select(".jobsearch-DesktopStickyContainer h3")
            if len(title) > 0:
                return title[0].text
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
    
    def _get_name(self, soup):
        
        try:    
            name = soup.select("*[class*='jobsearch-InlineCompanyRating'] div")
            if len(name) > 0:
                return name[0].text
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
        
    
    def _get_address(self,soup):
         try:
             address = soup.select("*[class*='jobsearch-JobMetadataHeader-iconLabel']")
             if len(address) > 0:
                 return address[0].text
             address = soup.select("*[class*='jobsearch-InlineCompanyRating'] div")
             if address[2].text == "-":
                 return address[3].text
             return address[2].text
         except Exception as e:
             address = soup.select("*[class*='jobsearch-InlineCompanyRating'] div")
             if address[2].text == "-":
                 return address[3].text
             return address[2].text
         
        
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

    def _get_contract_types_result(self, select_result):
        for item in select_result:
            if any(word in item.text.lower() for word in ["cdi","cdd","stage","alternance","temps plein","apprentissage","contrat pro"]):
                return item.text.strip()

    def _get_contract_type(self, soup):
        result = soup.select(".jobsearch-JobMetadataHeader-iconLabel")
        if len(result) > 0:
            return self._get_contract_types_result(result)
        return np.nan

    def _get_salary(self,soup, url):
        try:
            result = soup.select(".jobsearch-JobMetadataHeader-item")
            if len(result) > 0:
                return self._get_salary_result(result)

            result = soup.select(".jobsearch-JobMetadataHeader-itemWithIcon .jobsearch-JobMetadataHeader-iconLabel")
            if len(result) > 0:
                return self._get_salary_result(result)

            result = soup.select(".jobMetadataHeader-itemWithIcon-label")
            if len(result) > 0:
                return self._get_salary_result(result)

            result = soup.select("#jobDescriptionText")
            if len(result) > 0:
                outer_salary = re.compile(self.salary_pattern)
                m_salary = outer_salary.search(result[0].text)
                if m_salary is not None:
                    return self._get_salary_result(m_salary.group(0))
        
        except Exception as e:
            print(traceback.format_exc())
        return np.nan
    
    def _get_description(self,soup):
        try:
            e_description = soup.select(".jobsearch-JobComponent-description")
            if (len(e_description) > 0):
                return e_description[0].text
            return np.nan
        except Exception as e:
            print(traceback.format_exc())
    
    def _get_date(self,soup,url,name):
        #if name == np.nan:
        #    return np.nan
        try:
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
            
            if "jour" in label:
                date = date - timedelta(days=count)
            elif "heur" in label:
                date = date - timedelta(hours=count)
            return date;
        except Exception as e:
            print(traceback.format_exc())
    
    
    def parse(self,url):
        page = request.urlopen(url)
        soup = BeautifulSoup(page)
        
        title = self._get_title(soup)
        name = self._get_name(soup)
        if name == np.nan:
            print("name missing")
        address = self._get_address(soup)
        date = self._get_date(soup, url, name)
        description = self._get_description(soup)
        salary = self._get_salary(soup, url)
        contract_type = self._get_contract_type(soup)

        print("title -",title, "name -",name, "address -",address, "date -", date, "salary -",salary, "contract_type -",contract_type)
        return title, name, address, date, salary, description, contract_type


