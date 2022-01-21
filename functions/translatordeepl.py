import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
  
# url of the page to scrape
url = "https://www.deepl.com/en/translator#ja/en/DeepL%E3%81%B8%E3%82%88%E3%81%86%E3%81%93%E3%81%9D"
  
# initiating the webdriver.
driver = webdriver.Chrome('./chromedriver') 
driver.get(url) 
  
# this is just to ensure that the page is loaded
#time.sleep(5) 

#html = driver.page_source 
# renders the JS code and stores all
# of the information in static HTML code.

#apply bs4 to html variable
#soup = BeautifulSoup(html, "html.parser")
class_name = driver.find_element(By.CLASS_NAME, "lmt__textarea")
def deepl_translator(text):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    class_name.clear()
    class_name.send_keys(str(text)) # to be replaced by a variable
    all_divs = soup.find('div', {'id' : 'target-dummydiv'}) # this gets the translated text, continue with this tmr
    print(all_divs)
