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
def scrap_glisshop(keyword,paginas,archivo_json):
    diccionario = []

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (...) Safari/537.36")
    opts.add_argument("--window-position=1100,0")
    #opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get("https://www.glisshop.es/")
    sleep(3)

    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

    driver.get(f'https://www.glisshop.es/glisshop/resultado-de-la-busqueda-productos.html?searchText={keyword}')
    sleep(4)
    paginas_infinitas = (paginas == 0)
    i = 1
    while paginas_infinitas == True or i<=paginas:
        sleep(2)
        elementos = driver.find_elements(By.CLASS_NAME, 'df-card__main')
        num_elementos_pagina = len(elementos)

        for elemento in elementos:
            item_url = elemento.get_property('href')
            sku = re.search(r'(\d+)$', item_url).group(1)

            
            image_element = elemento.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('src')

            
            brand = elemento.find_element(By.CLASS_NAME, 'df-card__brand').text
            title = elemento.find_element(By.CLASS_NAME, 'df-card__title').text
            name = f"{brand} {title}"

        
            try:
                pvp = elemento.find_element(By.CLASS_NAME, 'df-card__price--old').text.replace(".","").replace(",", ".").replace("€","").strip()
                price = elemento.find_element(By.CLASS_NAME, 'df-card__price--new').text.replace(".","").replace(",", ".").replace("€","").strip()
            except Exception as e:
                
                price_padre = elemento.find_element(By.CLASS_NAME,'df-card__price--old-wrapper-price')
                price = price_padre.find_element(By.CLASS_NAME,'df-card__price ').text.replace(".","").replace(",", ".").replace("€","").strip()
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
        
        #boton_siguiente = driver.find_element(By.XPATH,f'//a[@data-page="{pagina}"]')
        #boton_siguiente.click()
        boton_siguiente = driver.find_element(By.XPATH, f'//a[@data-page="{i}"]')
        driver.execute_script("arguments[0].click();", boton_siguiente)

    # Guardar resultados
    with open(archivo_json + ".json", "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)

    print("Numero de productos encontrados:",len(diccionario))
    driver.quit()