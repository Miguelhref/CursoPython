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

def scrap_jack_jones(keyword, pages, json_file):
    results = []
    seen_skus = set()
    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    #opts.add_argument("--headless")  

    # Inicializar driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.jackjones.com/")
    sleep(3)

    # Aceptar cookies
    try:
        cookies_button = driver.find_element(By.CLASS_NAME,'cky-btn-accept').click()
        sleep(2)
    
        
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    #Voy a hacer 3 pasadas: "hombres","mujeres","niños"
    
    for x in range (1,4):
        for i in range (1,4):
            if x==1: #buscamos en "hombre"
                url = f'https://www.jackjones.com/es-es/search?q={keyword}&page={i}'
            elif x==2: #buscamos en "mujer"
                url = f'https://www.jackjones.com/es-es/jjxx/search?q={keyword}&page={i}'
            elif x==3:
                url = f'https://www.jackjones.com/es-es/ninos/search?q={keyword}&page={i}'
            driver.get(url)
            sleep(2)
            tree = HTMLParser(driver.page_source)
            elements = tree.css('article[data-v-9168b5ee]')
            for element in elements:
                sku = element.attrs.get('id')
                item_url = 'https://www.jackjones.com'+element.css_first('a[data-v-fe55a018]').attrs.get('href')
                image_url_raw= element.css_first('img').attrs.get('src')
                image_url = re.search(r".*?\.jpg", image_url_raw).group(0)
                
                name = element.css_first('.ellipsis').text().replace("'","").replace('\n',"").strip()
                #.text().replace("€","").replace(".","").replace(",",".").strip()
                try: 
                    pvp = element.css_first('.product-price__sales-price').text().replace("€","").replace(".","").replace(",",".").strip()
                    price = element.css_first('.product-price__discounted-price product-price__price-pad').text().replace("€","").replace(".","").replace(",",".").strip()
                except Exception as e:
                    price = element.css_first('.product-price__list-price').text().replace("€","").replace(".","").replace(",",".").strip()
                    pvp = None
                results.append({
                        "sku": sku,
                        "image_url": image_url,
                        "item_url": item_url,
                        "name": name,
                        "price": float(price),
                        "pvp": float(pvp) if pvp else None
                        })
