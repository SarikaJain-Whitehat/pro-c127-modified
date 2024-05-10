from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
service = webdriver.ChromeService(executable_path = 'E:/whitehat/SARIKA/PRO - C127/chromedriver-win64/chromedriver.exe')
browser = webdriver.Chrome(service=service)
#browser = webdriver.Chrome("")
browser.get(START_URL)

time.sleep(10)

planets_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")
        divContent=soup.find_all('div',{'class','hds-content-item'})

        '''
        # Loop to find element using XPATH
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):

            li_tags = ul_tag.find_all("li")
           
            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:                   
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            planets_data.append(temp_list)'''
        for div in divContent:

            temp=[]
            name=div.find_all('h3')[0].contents[0]
            temp.append(name)
            customFields=div.find_all('div',{'class','CustomField'})
            for customField in customFields:
                temp.append(customField.find_all('span')[1].contents[0])
            
            planets_data.append(temp)
        

        # Find all elements on the page and click to move to the next page
        #browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        #//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a
# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Define pandas DataFrame   
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

#//*[@id="primary"]/div/div[3]/div/div/div/div/div/div/div[2]/div[2]/nav/button[8]