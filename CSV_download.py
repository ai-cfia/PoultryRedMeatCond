#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import glob
import datetime
from shareplum import Office365
import os
import requests
#import selenium driver

try:
    from selenium import webdriver
except ImportError:
    print("selenium not installed, installing selenium")
    get_ipython().system('pip install selenium')
#load webdriver


try:
    driver = webdriver.Chrome("./chromedriver.exe")
except ImportError:
    print("Driver could not be loaded")

print("Driver now loaded to selenium")

try:
    driver.get("https://aimis-simia.agr.gc.ca/rp/index-eng.cfm?action=pR&pdctc=&r=278")
except:
    print('failed to load site and query')


driver.find_element_by_xpath('//*[@id="promptForm"]/div/input[11]').click()

#Load CSV file

while True:
    try:
        print("Attempting to download CSV file. Please do not download any other files")
        driver.find_element_by_xpath("//*[@id=\"wb-main-in\"]/p[2]/a[1]").click()
        break
    except:
        print("CSV not loaded. System sleep for 10 seconds")
        time.sleep(10)


count = 0
names_tags_of_files = [str(datetime.datetime.now()).replace("-","").split(" ")[0], "Report", "ADH"]
csv_in_folder = False

#Check if it is part of recent file

while True:
    try:
        list_of_files = glob.glob("./Downloads/*")
        five_newest_files = sorted(list_of_files, key = os.path.getctime)[-5:]

        for file in five_newest_files:
            if all(isinstance(item, str) for item in names_tags_of_files):
                csv_in_folder = True
                break
        if csv_in_folder == True:
            break
    except:
        print("check for file count :",  count)
print(five_newest_files)
if csv_in_folder:
    print("CSV downloaded to downloads folder")
else:
    sys.exit("Download Failed")
try:
    driver.get("https://collab.cfia-acia.inspection.gc.ca/cfia-acia/inspection/BIO/AH/_layouts/15/guestaccess.aspx?guestaccesstoken=PQ5mJWGr8ow4MvGL7nxHnAHmP6uu9b6TPCsH0qCO2xo%3d&folderid=2_15c8c3ab2c4d9448ebea30bee8e0a63e1&rev=1")
except:
    print('failed to load site and query')



try:
    print("Attempting to upload CSV file. Please do not download any other files")
    driver.find_element_by_xpath('//*[@id="QCB1_Button2"]').click()
except:
    print("CSV not uploaded")


    

