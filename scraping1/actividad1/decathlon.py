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

def scrap_decathlon(keyword, pages, json_file):
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
    driver.get("https://www.decathlon.es/es/")
    sleep(3)

    # Aceptar cookies
    try:
        driver.find_element(By.ID, "didomi-notice-agree-button").click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    i=0
    items = i*40
    while (i<pages or pages ==0):
        url =f'https://www.decathlon.es/es/search?Ntt={keyword}&from={items}&size=40'
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)
        sleep(2)
        elements = tree.css('div.product-block-top-main')
        sleep(1)
        for element in elements:
            
            
            item = element.css_first('a.vtmn-absolute')
            item_url ='https://www.decathlon.es'+ item.attrs.get('href')
            sku = re.search(r'R-p-([a-zA-Z0-9]+)', item_url).group(1)
            image_url = item.css_first('img').attributes.get('src')
            
            name = element.css_first('a.vtmn-block').text().strip()
            try: 
                pvp = element.css_first('span[aria-label="Precio anterior"]').text().replace("€","").replace(".","").replace(",",".").strip()
                price = element.css_first('span[aria-label="precio"]').text().replace("€","").replace(".","").replace(",",".").strip()
            except Exception as e:
                price = element.css_first('span[aria-label="precio"]').text().replace("€","").replace(".","").replace(",",".").strip()
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
    print("Número de productos encontrados en Decathlon:", len(results))  
    driver.quit()      