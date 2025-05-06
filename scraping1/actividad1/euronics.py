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

def scrap_euronics(keyword, pages, json_file):
    results = []
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.euronics.es")
    sleep(3)

    # Aceptar cookies
    try:
        
        accept_button = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        accept_button.click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)
    '''
    try:
        search_button = driver.find_element(By.ID,'txtBuscador')
        search_button.click()
        search_button.clear()
        search_button.send_keys(keyword)
        search_button.send_keys(Keys.RETURN)
        
    except Exception as e:
        print("Error al realizar la busqueda")
    '''
    sleep(3)
    driver.get(driver.current_url)
    i=0
    while (i<pages) or pages ==0:
        url = f'https://www.euronics.es/{keyword}.html?page={i}'
        driver.get(url)
        sleep(3)

        tree = HTMLParser(driver.page_source)
        elements = tree.css('.producto')
        for element in elements:
            try:
                sku_raw = tree.css_first('h2').css_first('a').attrs.get('onclick')
                sku = sku_raw.split(',')[1].strip()
                name = re.sub(r'\s+', ' ', element.css_first('h2').text()).strip()
                image_url= element.css_first('img').attrs.get('src')
                item_url = element.css_first('h2').css_first('a').attrs.get('href')
                price = re.sub(r'\s+', ' ', element.css_first('.precioProducto').text()).strip().replace('.',"").replace(',','.').replace('€','')
                
                pvp = None
                results.append({
                                "sku": sku,
                                "image_url": image_url,
                                "item_url": item_url,
                                "name": name,
                                "price": float(price),
                                "pvp": None
                            })
                   
            except Exception as e:
                #producto sin stock
                continue
        i+=1     
    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos únicos encontrados en Euronics:", len(results))
    driver.quit()    
        
           





   


      
                


        