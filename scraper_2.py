from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/Lists_of_stars"

browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

new_scraped_data = []

def scrape_more_data (hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []

        for tr_tag in soup.find_all ("tr",sttrs = {"class":"fact_row"}):

            for td_tag in td_tag:
                try:
                    temp_list.append(td_tag.find_all ("div", attrs = {"class": "value"}))
                except:
                    temp_list.append("")
        new_scraped_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape_df_1 = pd.read_csv("scraped_data.csv")

for index, row in scrape_df_1.iterrows ():
    print (row ['hyperlink'])
    print (f"Data Scraping at hyperlink {index + 1} completed")

scraped_data = []

for row in new_scraped_data:
    replaced = []
    for el in row:
        el = el.replaced ("\n","")
        replaced.append(el)
    scraped_data.append(replaced)

print(scraped_data)