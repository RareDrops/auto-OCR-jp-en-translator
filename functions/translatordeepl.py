import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
  
# url of the page to scrape
url = "https://www.deepl.com/en/translator#ja/en/DeepL%E3%81%B8%E3%82%88%E3%81%86%E3%81%93%E3%81%9D"
  
# initiating the webdriver.
driver = webdriver.Chrome('./chromedriver')
driver.get(url) 
  
# this is just to ensure that the page is loaded
#time.sleep(5) 

html = driver.page_source 
# renders the JS code and stores all
# of the information in static HTML code.

#apply bs4 to html variable
#soup = BeautifulSoup(html, "html.parser")
class_name = driver.find_element(By.CLASS_NAME, "lmt__textarea")
def deepl_translator(text):
    class_name.clear()
    class_name.send_keys(str(text)) # to be replaced by a variable
    time.sleep(3)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find('div', {'id' : 'target-dummydiv'}) # this gets the translated text, continue with this tmr
    return all_divs.get_text()
