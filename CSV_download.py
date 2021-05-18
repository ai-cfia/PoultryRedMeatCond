#!/usr/bin/env python
# coding: utf-8



import time
import glob
import datetime
import os
import requests
import sys
import shutil
#import selenium driver

try:
    from selenium import webdriver
except ImportError:
    print("selenium not installed, installing selenium")
    get_ipython().system('pip install selenium')
#load webdriver


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
    


try:
    data_path =  os.getcwd() + "\\data\\"
    prefs = {'download.default_directory' : data_path}

    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome("./chromedriver.exe", chrome_options=chrome_options)


    
    
except ImportError:
    print("Driver could not be loaded")

print("Driver now loaded to selenium")



try:
    driver.get("https://aimis-simia.agr.gc.ca/rp/index-eng.cfm?action=pR&pdctc=&r=278")
except:
    print('failed to load site and query')

#remove old CSV file

#files = glob.glob('./data/*.csv')
# if len(files) > 0:
#     print("removing old csv file")
#     for f in files:
#         os.remove(f)

    
    
options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=D:/Sele_Downloads")
    

driver.find_element_by_xpath('//*[@id="promptForm"]/div/input[11]').click()
count = 0
#Load CSV file

while True:
    try:
        print("Attempting to download CSV file. Please do not download any other files")
        driver.find_element_by_xpath("/html/body/main/p[2]/a[1]").click()
        break
    except:
        print("CSV not loaded. System sleep for 10 seconds")
        time.sleep(10)
        if count == 100:
            sys.exit("Failed to Download")
    count += 1
    
print("File succesfully downloaded. Saving the file to correct title")
time.sleep(10)
list_of_files = glob.glob(data_path + "*.csv") # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

shutil.copy(latest_file , data_path + "\\ADH-717 - Poultry and Red Meat data.csv")


    
