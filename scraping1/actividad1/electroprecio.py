import io
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
def scrap_electroprecio(keyword,paginas,archivo_json):
    diccionario = []

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (...) Safari/537.36")
    opts.add_argument("--window-position=1100,0")
    opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get("https://www.electroprecio.com/")
    sleep(3)
    keyword = 'televisor'
    paginas = 3

    driver.find_element(By.CLASS_NAME,'btn-primary').click()
    paginas_infinitas = (paginas == 0)
    i = 1
    driver.get(f'https://www.electroprecio.com/catalogsearch/result/?p={i}&q={keyword}')

    while paginas_infinitas == True or i<=paginas:
        sleep(2)

        elementos = driver.find_elements(By.CLASS_NAME,'single-product')
        for elemento in elementos:
            sku_raw = elemento.find_element(By.TAG_NAME,'img').get_property('id')
            
            sku = re.search(r'(\d+)$', sku_raw).group(1)
            image_url = elemento.find_element(By.TAG_NAME,'img').get_property('src')
            elemento_a=elemento.find_element(By.TAG_NAME,'a')
            
            item_url = elemento_a.get_property('href')
            name = elemento_a.get_property('title')
            try:
                price_raw = elemento.find_element(By.CLASS_NAME,f'old-price').text
                pvp = re.search(r'\d+,\d+|\d+\.\d+', price_raw.replace(".", "").replace(",", ".")).group()
                price = elemento.find_element(By.CLASS_NAME,f'special-price').text.replace(".","").replace(",", ".").replace("€","").strip()
            except Exception as e:
                price_padre = elemento.find_element(By.CLASS_NAME,'regular-price')
                price = price_padre.find_element(By.CLASS_NAME,'price').text.replace(".","").replace(",", ".").replace("€","").strip()
                pvp = None
            diccionario.append({
                        "sku": sku,
                        "image_url": image_url,
                        "item_url": item_url,
                        "name": name,
                        "price": price,
                        "pvp": pvp
                    })
            
        i = i+1
        try:
            boton_siguiente = driver.find_element(By.CLASS_NAME,'next')
            boton_siguiente.click()
        except Exception as e:
            break
     # Guardar resultados
    with open(archivo_json + ".json", "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)

    print("Numero de productos encontrados en electroprecio:",len(diccionario))
    driver.quit()
    