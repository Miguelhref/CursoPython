from bs4 import BeautifulSoup
import requests
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
url = 'https://www.dosfarma.com/'

response = requests.get(url)

soup = BeautifulSoup(response.text,'html.parser')
opts = Options()
opts.add_argument("user-agent=...")
opts.add_argument("--window-position=1100,0")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)
#opts.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

driver.get('https://www.dosfarma.com/')
sleep(3)
try:
        driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
        sleep(3)
except Exception as e:
          print('Cookie error')
keyword = 'solar'

pages = 3
response = ''
for i in range (1,pages+1):
        url = f'https://www.dosfarma.com/catalogsearch/result/?q={keyword}&page={i}'
        page_response =response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

        response += page_response

soup = BeautifulSoup(response, 'html.parser')
elements = soup.find_all('li','class="ais-Hits-item product"')
print(soup)
       

