from bs4 import BeautifulSoup
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
driver = webdriver.Chrome(options=options)
driver.get(url)


# renders the JS code and stores all
# of the information in static HTML code.
html = driver.page_source

class_name = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @role='textbox' and @aria-multiline='true']")
def deepl_translator(text):
    class_name.clear()
    class_name.send_keys(str(text))
    time.sleep(config.getint('translator','time_wait_to_translate'))
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    target_elements = soup.findAll('span', {'class': '--l --r sentence_highlight'})
    raw_text = target_elements[0].get_text()
    translated_text = target_elements[1].get_text()
    if translated_text == None:
        return
    return (raw_text, translated_text)
