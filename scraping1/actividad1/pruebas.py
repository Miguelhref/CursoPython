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
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
}
chrome_options = Options()
chrome_options.add_argument(f"user-agent={headers['User-Agent']}")

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.fnac.es/iphone?PageIndex=1&SDM=list')
time.sleep(30) 

page_source = driver.page_source
print(page_source)

driver.quit()
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import random

# Configuración de Chrome con evasión de detección
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36")
opts.add_argument("--window-position=1100,0")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
#opts.add_experimental_option('useAutomationExtension', False)

# Inicializa el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Evasión del `navigator.webdriver`
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})
for i in range(1,50):
    # Visita Fnac y espera a que cargue
    driver.get("https://www.fnac.es/")
    print("Prueba numero:",i)
    sleep(5)  # Espera aleatoria tipo humano