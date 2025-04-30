import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.parser import HTMLParser

def scrap_atida(keyword, pages, json_file):
    results = []
    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    #opts.add_argument("--headless")  

    # Inicializar driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.atida.com/")
    sleep(3)

    # Aceptar cookies
    try:
        driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)
    i=1
    while (i<=pages or pages ==0):
        url =f'https://www.atida.com/es-es/catalogsearch/result/?q={keyword}&page={i}'
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)
        sleep(2)
        elements = tree.css('div[itemprop="itemListElement"]')
        for element in elements:
            item = element.css_first('a')
            sku = item.attrs.get('data-objectid')
            image_url_raw = item.css_first('source')
            image_url_args = image_url_raw.attrs.get('srcset').split(" ")
            image_url = image_url_args[2]
            item_url =item.attrs.get('href')
            name = element.css_first('div.ais-Hits-item__name-wrap').text().strip()
            try: 
                pvp = element.css_first('span.line-through').text().replace("\xa0€","").replace(".","").replace(",",".").strip()
                price = element.css_first('span.promotion').text().replace("\xa0€","").replace(".","").replace(",",".").strip()
            except Exception as e:
                price = element.css_first('span.whitespace-nowrap').text().replace("\xa0€","").replace(".","").replace(",",".").strip()
                pvp = None
            results.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": float(price),
                    "pvp": float(pvp) if pvp else None
                    })
        i+=1        
    # Guardar resultados
    with open(json_file + ".json", "w", encoding="utf-8") as f:
    
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Número de productos encontrados en Atida:", len(results))  
    driver.quit()  