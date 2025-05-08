import json
import time
from time import sleep
import re
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def scrap_ldlc(keyword, pages, json_file):
    results = []
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    #opts.add_argument("--headless")  
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.ldlc.com/es-es/")
    sleep(3)

    # Aceptar cookies
    try:
        
        accept_button = driver.find_element(By.ID, 'cookieConsentAcceptButton')
        accept_button.click()
        sleep(2)
    except Exception as e:
        print('Error al aceptar las cookies')
    
    i=1
    while (i<pages+1) or pages ==0:
        if i == 1:
            url = f'https://www.ldlc.com/es-es/buscar/{keyword}/'
        else:    
            url = f'https://www.ldlc.com/es-es/buscar/{keyword}/page{i}/'
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)
        elements = tree.css('li.pdt-item')
        for element in elements:

            sku= element.attrs.get('data-id')
            image_url = 'https://www.ldlc.com'+ element.css_first('a').attrs.get('href')
            item_url = element.css_first('a img').attrs.get('src')
            name= element.css_first('a img').attrs.get('alt')
            
            price_raw = element.css_first('.price').text()
            price  = price_raw####Falta acabar esto, hubo un error al guardar
            pvp = None
            results.append({
                            "sku": sku,
                            "image_url": image_url,
                            "item_url": item_url,
                            "name": name,
                            "price": float(price),
                            "pvp": pvp
                        })
        i+=1
    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en hp:", len(results))
    driver.quit()
        