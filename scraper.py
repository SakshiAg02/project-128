from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


START_URL = "https://en.wikipedia.org/wiki/Lists_of_stars"

browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")

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

            scraped_data.append(temp_list)

        # Find all elements on the page and click to move to the next page
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

soup = BeautifulSoup(browser.page_source, "html.parser")

bright_star_table = soup.find ("table",attrs = {"class", "wikitable"})
table_body = bright_star_table.find ('tbody')
table_rows = table_body.find_all ('tr')

for row in table_rows:
    table_cols = row.find_all ('td')
    print (table_cols) 
    temp_list = []
    for col_data in table_cols:
        # print (col_data.text)
        data = col_data.text.strip ()
        # print (data)
        temp_list.append (data)
        scraped_data.append (temp_list)

stars_data = []

for i in range (0,len (scraped_data)):
    Star_names = scraped_data [i][1]
    Distance = scraped_data [i][3]
    Mass = scraped_data [i][5]
    Radius = scraped_data [i][6]
    Lum = scraped_data [i][7]
    
    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append (required_data)
    
    headers = ['Star_name','Distance','Mass','Radius','Luminosity']
    star_df_1 = pd.DataFrame (stars_data, columns = headers)
    star_df_1.to_csv ('scrapped_data.csv',index = True, index_label = "id")