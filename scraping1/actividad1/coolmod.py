import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#def scrap_deporte_outlet(keyword, pages, json_file):
keyword = "monitor"
pages = 3
json_file = f'{keyword}_coolmod'
results = []
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36")
opts.add_argument("--window-position=1100,0")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)
#opts.add_argument("--headless")  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

try:

    driver.get('https://www.coolmod.com/')
    sleep(3)


    try:
        driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
        sleep(5)
    except:
        pass

    infinite_pages = (pages == 0)
    i = 1
    while (infinite_pages or i<=pages):

        url = f'https://www.coolmod.com/?gad_source=1&gbraid=0AAAAAD_BC_PFg4lIqxGCYG2kCslqo3iDD&gclid=Cj0KCQjw5azABhD1ARIsAA0WFUF8wM_dzdNxl9yPD8cjbidkn6sY3jUmuV8M-Vp4xtJmuxnrerRz3P4aAr0iEALw_wcB#01cc/fullscreen/m=and&p=4&q=monitor'
except Exception as e:
    print()