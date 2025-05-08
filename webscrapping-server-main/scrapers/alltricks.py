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

def scrap_alltricks(keyword, pages, json_file):
    results = []
    skus_seen = set()  #  Para evitar duplicados

    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--headless")  

    # Inicializar driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.alltricks.es/")
    sleep(3)

    # Aceptar cookies
    try:
        driver.find_element(By.ID, "didomi-notice-agree-button").click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    # Buscar producto
    input = driver.find_elements(By.CLASS_NAME, "tt-input")[1]
    input.click()
    sleep(1)
    #Hago un bucle de intentos para el input ya que a veces falla al primer intento
    for i in range(1,5):
        try:
            input = driver.find_element(By.CLASS_NAME, "sf-search-input-field--with-delete")
            input.send_keys(keyword)
            input.send_keys(Keys.RETURN)
            break
        except Exception as e:
            continue
    sleep(3)

    # Contenedor con scroll
    scroll_container = driver.find_element(By.CSS_SELECTOR, '.sf-main-container.sf-scroll')
    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

    i = 1
    while i <= pages or pages == 0:
        tree = HTMLParser(driver.page_source)
        elements = tree.css(".sf-product__border--none")

        for element in elements:
            try:
                item_url = element.attrs.get("href")
                sku_match = re.search(r'P-(\d+)', item_url)
                sku = sku_match.group(1) if sku_match else None

                if not sku or sku in skus_seen:
                    continue  # 🚫 Saltar duplicados o sin SKU

                image_url_raw = element.css_first('.sf-product-image__image')
                image_url = image_url_raw.attrs.get('src') if image_url_raw else None

                name_el = element.css_first('.sf-product__title')
                name = name_el.text() if name_el else None

                price_raw = element.css_first('.sf-price-root').text()
                price_match = re.search(r'\d+,\d+', price_raw)
                price = price_match.group(0).replace(".", "").replace(",", ".") if price_match else None

                pvp_raw = element.css_first('.sf-price-ppc').text()
                pvp_match = re.search(r'\d+,\d+', pvp_raw)
                pvp = pvp_match.group(0).replace(".", "").replace(",", ".") if pvp_match else None

                results.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": float(price),
                    "pvp": float(pvp) if pvp else None
                    })

                skus_seen.add(sku)  # ✅ Marcar como procesado
            except Exception as e:
                print(f"Error al procesar producto: {e}")

        # Scroll
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        sleep(3)

        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        if pages == 0 and new_height == last_height:
            break
        last_height = new_height
        i += 1

    # Guardar resultados
    with open(json_file + ".json", "w", encoding="utf-8") as f:
    
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Número de productos encontrados en Alltricks:", len(results))  
    driver.quit()  


