import time
import glob
import os
from github import Github
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import subprocess

load_dotenv()

def setup_webdriver(download_path):
    """Set up and return a Chrome WebDriver with specified options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--enable-features=NetworkServiceInProcess")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_experimental_option("prefs", {'download.default_directory': download_path})
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def wait_for_download(download_path, timeout=30):
    """Wait for the download to start and complete, returning True if successful."""
    download_started = False
    time.sleep(10)
    while timeout > 0:
        files = glob.glob(f"{download_path}/*")
        if files and all(not f.endswith('.crdownload') for f in files):
            download_started = True
            break
        time.sleep(1)
        timeout -= 1
    return download_started and timeout > 0

def handle_frontend_interaction(driver, URL):
    """Handles front-end interactions including navigating, CAPTCHA solving, and initiating download."""
    
    driver.get(URL)
    driver.implicitly_wait(20)
    captcha_text = driver.find_element(by='id', value='captcha_label').text
    captcha_answer = eval(captcha_text.split('=')[0])
    driver.find_element(by='id', value='captcha').send_keys(str(captcha_answer))
    driver.find_element(by='id', value='btnNext').click()
    driver.find_element(by='id', value='linkGetReport').click()
    
def merge_reports(new_report):
    print('\033[2;31;43m MERGING REPORTS \033[0;0m')

    # Load the data
    MASTERLIST_URL = os.getenv('MASTERLIST_URL')
    master_dataframe = pd.read_csv(MASTERLIST_URL, encoding="utf-16", delimiter="\t")
    monthly_dataframe = pd.read_csv(new_report, encoding="utf-16", delimiter="\t")

    # Ensure the 'Year' column is of type integer
    master_dataframe['Year'] = master_dataframe['Year'].astype(int)
    monthly_dataframe['Year'] = monthly_dataframe['Year'].astype(int)

    # Define the key columns for matching
    key_columns = ['Year', 'Month_ID', 'Region_Province_Eng', 'Region_Province_Fr', 'Species_Eng', 'Species_Fr', 'Type_Eng', 'Type_Fr', 'Condition_Code', 'Description_Eng', 'Description_Fr', 'Units_Eng', 'Units_Fr']
    
    # Merge to update existing rows
    merged_dataframe = pd.merge(master_dataframe, monthly_dataframe[key_columns + ['Data_Value']], on=key_columns, how='left', suffixes=('', '_new'))
    merged_dataframe['Data_Value'] = merged_dataframe.apply(lambda x: x['Data_Value_new'] if pd.notnull(x['Data_Value_new']) else x['Data_Value'], axis=1)
    merged_dataframe.drop(columns=['Data_Value_new'], inplace=True)

    # Identify and add new rows
    new_rows = monthly_dataframe[~monthly_dataframe[key_columns].apply(tuple, 1).isin(master_dataframe[key_columns].apply(tuple, 1))]
    updated_master_dataframe = pd.concat([merged_dataframe, new_rows], ignore_index=True)

    # Sort immediately before saving
    updated_master_dataframe.sort_values(by=['Species_Eng', 'Year'], inplace=True)
    updated_master_dataframe = updated_master_dataframe.drop_duplicates(subset=key_columns)

    # Save the updated master list
    file_path = os.path.join('.', 'data', 'ADH-717 - Poultry and Red Meat data.csv')
    updated_master_dataframe.to_csv(file_path, index=False, encoding="utf-16", sep="\t")

    print('Updated master dataframe shape:', updated_master_dataframe.shape)
    print('\033[2;31;43m MERGED REPORTS SUCCESSFULLY \033[0;0m')

def update_github(commit_message="Updated the master list"):
    """Commit and push changes to GitHub."""
    print('\033[2;31;43m UPDATING GITHUB \033[0;0m')
    pass 

def main():
    """Main function to retrieve the CSV report."""

    try:
        NEW_REPORT_URL = os.getenv('NEW_REPORT_URL')
        data_path = os.path.join(os.getcwd(), "data")

        driver = setup_webdriver(data_path)
        handle_frontend_interaction(driver, NEW_REPORT_URL)

        if wait_for_download(data_path):

            report_files = glob.glob(f"{data_path}/Report*")
            if report_files:
                # Since there's only ever one, we can take the first match
                merge_reports(new_report=report_files[0])
                os.remove(report_files[0])
                
            else:
                print("No 'Report' file found in the data folder.")
        else:
            print("Download did not start or complete in time.")
        

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed to retrieve data'
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
