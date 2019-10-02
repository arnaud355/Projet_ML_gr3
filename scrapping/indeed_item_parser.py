from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time

class IndeedItemParser:
    def __init__(self):
        self.driverPath = "C:\\Users\\Junior\\Documents\\selenium\\driver\\chromedriver.exe"
        
    def _get_title(self, driver):
        try:
            title = driver.find_element_by_xpath("//*[@class='jobsearch-DesktopStickyContainer']//h3")
        except Exception as e:
            print(e)
        return title.text
    
    def _get_name(self, driver):
        
        try:    
            name = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[1]")
            return name.text
        except Exception as e:
            print(e)
        
    
    def _get_address(self,driver):
         try:   
            address = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[3]")
            if address.text == "-":
                address = driver.find_element_by_xpath("//*[contains(@class,'jobsearch-InlineCompanyRating')]//div[4]")
            return address.text
         except Exception as e:
            address = driver.find_element_by_xpath("//span[@class='jobsearch-JobMetadataHeader-iconLabel'][1]")
            return address.text
    
    def _get_description(self,driver):
        try:
            #jobDescriptionText
            e_description = driver.find_element_by_id("jobDescriptionText")
            return e_description.get_attribute('innerHTML')
        except Exception as e:
            print(e)
    
    def _get_date(self,driver,url,name):
       # print(url)
        try:
            date_str = driver.find_element_by_xpath("//*[@class='jobsearch-JobMetadataFooter']")
            date_str_full = date_str.text
            date_tbl = date_str_full.split(" ")
            count_str = date_tbl[4]
            label = date_tbl[5]
            
            if name in date_str_full:
                date_str_full = date_str_full.replace(name, "")
                date_tbl = date_str_full.split(" ")
                count_str = date_tbl[5]
                label = date_tbl[6]
                
            if count_str == "a" :
                count_str = date_tbl[5]
                label = date_tbl[6]
                
            #print("date_str", date_tbl)
            date = datetime.now()
            
            if count_str == "30+":
                return date - timedelta(days=30)
            
            count = int(count_str)
            if "jour" in label:
                date = date - timedelta(days=count)
            elif "heur" in label:
                date = date - timedelta(hours=count)
            return date;
        except Exception as e:
            print(e)
    
    
    def parse(self,url):
        driver = webdriver.Chrome(self.driverPath)
        driver.get(url)
        driver.maximize_window()
        
        title = self._get_title(driver)
        name = self._get_name(driver)
        address = self._get_address(driver)
        date = self._get_date(driver, url,name)
        description = self._get_description(driver)
        
        #driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=description))
        #xx = driver.find_elements_by_tag_name("p")
        #print("len(xx) : ",len(xx))
        
        driver.close()
        
        return title, name, address, date, description