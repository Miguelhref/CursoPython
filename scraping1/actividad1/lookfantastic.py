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

def scrap_lookfantastic(keyword, pages, json_file):
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
    driver.get("https://www.lookfantastic.es/")
    sleep(3)

    # Aceptar cookies
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    i=1
    while (i<=pages or pages ==0):
        url =f'https://www.lookfantastic.es/search/?q={keyword}&pageNumber={i}'
        driver.get(url)
        tree = HTMLParser(driver.page_source)
        elements = tree.css('product-card-wrapper')
        for element in elements:
            sku = element.attrs.get('data-quicklook')
            a_tag = element.css_first('a')
            item_url = 'https://www.lookfantastic.es'+a_tag.attrs.get('href') 
            name = a_tag.attrs.get('data-title')
            image_url_raw = element.css_first('source')
            image_url = image_url_raw.attrs.get('srcset') 
            price_p = element.css_first('.override-price-style')
            pvp = None
            try:
                pvp_raw = price_p.css_first('.mt-6').text().replace(".", "").replace(",", ".").replace("€","")
                pvp = pvp_raw if pvp_raw else None
                price= price_p.css_first('.text-gray-900').text().replace(".", "").replace(",", ".").replace("€","")
            except Exception as e:
                price = price_p.text().replace(".", "").replace(",", ".").replace("€","")
            
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
    print("Número de productos encontrados en Lokkfantastic:", len(results))  
    driver.quit()  