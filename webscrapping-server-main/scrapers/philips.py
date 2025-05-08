from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Opciones
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (...) Safari/537.36")
opts.add_argument("--window-position=1100,0")
#opts.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

driver.get("https://www.philips.es/")

sleep(3)


iframe = driver.find_element(By.CSS_SELECTOR,'iframe[src*="consent"]')

driver.switch_to.frame(iframe)

boton = driver.find_element(By.CSS_SELECTOR, ".pdynamicbutton .call")
boton.click()


driver.switch_to.default_content()