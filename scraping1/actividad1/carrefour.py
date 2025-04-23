import io
import json
import time
import re
from time import sleep
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# opts.add_argument("--headless")
diccionario = []
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

url = 'https://www.carrefour.es/'
driver.get(url)
sleep(3)


try:
    aceptar_cookies = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    aceptar_cookies.click()
    sleep(3)
except Exception as e:
    print('Error al aceptar las cookies')
    print(e)

#def search(keyword):
keyword = "iphone"
while (True):
    typetextfirst = driver.find_element(By.CLASS_NAME,"x-search-input x-input x-ml-0 x-pl-8")
    typetextfirst.clear()
    typetextfirst.send_keys(keyword)
    cargar_mas =driver.find_element(By.XPATH,'//button[@aria-label = "Load"]')
    #tree = HTMLParser(driver.page_source)
    elementos = driver.find_elements(By.TAG_NAME,'article')
    for elemento in elementos:

        sku_raw = driver.find_element(By.CLASS_NAME,'href')
        sku = re.search(r'/(\d{13})/', sku_raw)


        '''
        Guardar los siguientes datos para cada producto:
● sku → ID del producto
● image_url → URL de la imagen del producto
● item_url → URL de la página del producto
● name → Nombre del producto
● price → Precio actual del producto (tipo float)
● pvp → Precio anterior (si existe; si no, None, tipo float)

● Eliminación de símbolos de moneda (€, $, etc.).
● El número debe tener un solo punto decimal (por ejemplo, 1.000,94 debe convertirse a 1000.94).
        '''
    cargar_mas.click()

