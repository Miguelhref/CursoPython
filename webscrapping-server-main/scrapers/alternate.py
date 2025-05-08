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

def scrap_alternate(keyword, pages, json_file):
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
    driver.get("https://www.alternate.es/")
    sleep(3)

    # Aceptar cookies
    cookies_button = driver.find_element(By.ID, 'usercentrics-cmp-ui')
    cookies_button_shadow = driver.execute_script('return arguments[0].shadowRoot', cookies_button)
    try:
        cookies_button_shadow.find_element(By.ID, 'accept').click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    i = 1
    while i <= pages or pages == 0:
        url = f'https://www.alternate.es/listing.xhtml?q={keyword}&page={i}'
        driver.get(url)
        sleep(2)
        tree = HTMLParser(driver.page_source)
        sleep(2)
        root_element = tree.css_first('.grid-container')
        elements = root_element.css('a')
        
        sleep(1)
        for element in elements:
            item_url = element.attrs.get('href')
            match = re.search(r'/product/(\d+)$', item_url)
            if not match:
                continue
            sku = match.group(1)

            if sku in seen_skus:  # <-- Evita duplicados
                continue
            seen_skus.add(sku)

            name = element.css_first('img').attrs.get('alt')
            image_url = 'https://www.alternate.es' + element.css_first('img').attrs.get('src')
            try:
                pvp = element.css_first('.line-through').text().replace("€", "").replace(".", "").replace(",", ".").strip()
                price = element.css_first('.price').text().replace("€", "").replace(".", "").replace(",", ".").strip()
            except Exception:
                price = element.css_first('.price').text().replace("€", "").replace(".", "").replace(",", ".").strip()
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
    print("Número de productos encontrados en Alternate:", len(results))
    driver.quit()
