from bs4 import BeautifulSoup
from gevent import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from configparser import ConfigParser
#loads the configuration file and reads it
config = ConfigParser()
config.read('config.ini')




# url of the page to scrape
url = "https://www.deepl.com/en/translator#ja/en/DeepL%E3%81%B8%E3%82%88%E3%81%86%E3%81%93%E3%81%9D"
  
# initiating the webdriver.
if config.getboolean('main','show_chrome_window') == False:
    options = Options()
    options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver', options=options)
driver.get(url)


# renders the JS code and stores all
# of the information in static HTML code.
html = driver.page_source 

class_name = driver.find_element(By.CLASS_NAME, "lmt__textarea")
def deepl_translator(text):
    class_name.clear()
    class_name.send_keys(str(text))
    time.sleep(config.getint('translator','time_wait_to_translate'))
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find('div', {'id' : 'target-dummydiv'})
    return all_divs.get_text()
