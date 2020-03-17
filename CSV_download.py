#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import glob
import datetime
import os
import requests
import sys
#import selenium driver

try:
    from selenium import webdriver
except ImportError:
    print("selenium not installed, installing selenium")
    get_ipython().system('pip install selenium')
#load webdriver


def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

    


try:
    driver = webdriver.Chrome("./chromedriver.exe")
except ImportError:
    print("Driver could not be loaded")

print("Driver now loaded to selenium")
enable_download_headless(driver, "./data/")



try:
    driver.get("https://aimis-simia.agr.gc.ca/rp/index-eng.cfm?action=pR&pdctc=&r=278")
except:
    print('failed to load site and query')

#remove old CSV file

files = glob.glob('./data/*.csv')
if len(files) > 0:
    print("removing old csv file")
    for f in files:
        os.remove(f)

    
    
options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=D:/Sele_Downloads")
    

driver.find_element_by_xpath('//*[@id="promptForm"]/div/input[11]').click()
count = 0
#Load CSV file

while True:
    try:
        print("Attempting to download CSV file. Please do not download any other files")
        driver.find_element_by_xpath("//*[@id=\"wb-main-in\"]/p[2]/a[1]").click()
        break
    except:
        print("CSV not loaded. System sleep for 10 seconds")
        time.sleep(10)
        if count == 100:
            sys.exit("Failed to Download")
    count += 1

    
