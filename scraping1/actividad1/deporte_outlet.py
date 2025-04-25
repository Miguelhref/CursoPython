import io
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re

keyword = 'nike'
pages = 3
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36")
opts.add_argument("--window-position=1100,0")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)
#opts.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url = 'https://www.deporte-outlet.es/'
driver.get(url)
sleep(3)
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
infinite_pages = (pages==0)

for i in range(1,pages+1):
    url= f'https://www.deporte-outlet.es/search?sSearch=ni{keyword}&p={i}'

    driver.get(url)

    elements = driver.find_elements(By.CLASS_NAME,'box--minimal')

    for element in elements:

        sku = element.get_attribute('data-ordernumber')
        image_url = element.find_element(By.TAG_NAME,'img').get_attribute('srcset')
        item_url = element.find_element(By.TAG_NAME,'a').get_attribute('href')
        name = element.find_element(By.TAG_NAME,'a').get_attribute('title')
        price_int= element.find_element(By.CLASS_NAME,'price--default-lineheight').text.replace(",",".").replace("€","")
        price_dec= element.find_element(By.CLASS_NAME,'price--default-sup').text.replace(",",".").replace("€","")
        price = f'{price_int}{price_dec}'
        pvp= element.find_element(By.TAG_NAME,'del').text.replace(",",".").replace("€","")


