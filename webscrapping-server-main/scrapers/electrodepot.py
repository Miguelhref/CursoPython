import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.parser import HTMLParser
import selectolax
import re
def scrap_electrodepot(keyword, pages, json_file):
    results = []
    
    opts = Options()
    opts.add_argument("user-agent=...")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get('https://www.electrodepot.es/')
    sleep(3)

    try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            sleep(3)
    except Exception as e:
          print('Cookie error')
    for i in range(1,pages+1) or pages ==0:    

        url = f'https://www.electrodepot.es/catalogsearch/result/?q={keyword}&page={i}'
        
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)

        elements = tree.css('div.productlist-item_block')
        if len(elements)==0: break
        sleep(2)
        for element in elements:
               
                
                image_url_raw = element.css_first('img')
                image_url = image_url_raw.attrs.get('src')
                sku = re.search(r'P(\d+)\.jpg', image_url).group(1)
                item_url_raw = element.css_first('a')
                item_url = item_url_raw.attrs.get('href')
                name = image_url_raw.attrs.get('title')

              
                pvp = None
                
                price_raw = element.css_first('.number_price').text().replace(".", "").replace("€", ".")
                price =   price_raw.rstrip('.')
              
                results.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": float(price),
                    "pvp": float(pvp) if pvp else None
                    })

    with open(json_file + ".json", "w", encoding="utf-8") as f:
    
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en electrodepot:", len(results))  
    driver.quit()          
                