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

def scrap_douglas(keyword, pages, json_file):
    results = []
    seen_skus = set()
    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--headless")  

    # Inicializar driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.douglas.es/")
    sleep(3)

    # Aceptar cookies
    cookies_button = driver.find_element(By.ID, 'usercentrics-root')
    cookies_button_shadow = driver.execute_script('return arguments[0].shadowRoot', cookies_button)

    try:
   
        accept_button = cookies_button_shadow.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
        accept_button.click()
        sleep(2)
    
        
    except Exception as e:
        print("Error al aceptar las cookies:", e)

       

    i = 1
    while i <= pages or pages == 0:
        url = f'https://www.douglas.es/es/search?q={keyword}&page={i}'
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)
        sleep(2)
        
        elements = tree.css('div[data-testid="product-tile"]')
        
        sleep(2)
        for element in elements:
            item_url = 'https://www.douglas.es'+element.css_first('a').attrs.get('href')
            sku = re.search(r'/p/(\d+)', item_url).group(1)
           


            if sku in seen_skus:  
                break
            seen_skus.add(sku)
            name_temp =''
            texts = element.css('.text')
            for i in range(0,3):
                name_temp += texts[i].text().strip() +' ' 
            name = name_temp.strip()
            image_url = element.css_first('img').attrs.get('alt')

            # .text().replace("€", "").replace(".", "").replace(",", ".").strip()
            try:
                price_block = element.css('.product-price__price')
                pvp = price_block[0].text().replace("€", "").replace(".", "").replace(",", ".").strip()
                price = price_block[1].text().replace("€", "").replace(".", "").replace(",", ".").strip()
            except Exception:
                price = price_block[0].text().replace("€", "").replace(".", "").replace(",", ".").strip()
                pvp = None
            results.append({
                "sku": sku,
                "image_url": image_url,
                "item_url": item_url,
                "name": name,
                "price": float(price),
                "pvp": float(pvp) if pvp else None
            })
        i += 1

    # Guardar resultados
    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Número de productos encontrados en Douglas:", len(results))
    driver.quit()
