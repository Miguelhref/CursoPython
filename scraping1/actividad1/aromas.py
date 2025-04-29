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
def scrap_aromas(keyword, pages, json_file):
    results = []
    
    opts = Options()
    opts.add_argument("user-agent=...")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get('https://www.aromas.es/')
    sleep(3)
    try:
            driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
            sleep(3)
    except Exception as e:
          print('Cookie error')

#He observado que aromas al hacer scroll carga una url donde dice el item inicial y el final para cargar de 12 en 12. 
#Cogere el numero de paginas pedidas, lo multiplicare por 12 y mostrare todos los items hasta ese
#En caso de pedir 0 paginas, motraremos un maximo de 10000 items
    num_items = pages*12
    if pages ==0:
          url = f'https://www.aromas.es/Actualizar-filtro?q={keyword}&start=0&sz=2000&selectedUrl=https%3A%2F%2Fwww.aromas.es%2FActualizar-filtro%3Fq%3Dlapiz%26start%3D24%26sz%3D12'
    else:
          url = f'https://www.aromas.es/Actualizar-filtro?q={keyword}&start=0&sz={num_items}&selectedUrl=https%3A%2F%2Fwww.aromas.es%2FActualizar-filtro%3Fq%3Dlapiz%26start%3D24%26sz%3D12'
    
    driver.get(url)
   
    tree = HTMLParser(driver.page_source)

    elements = tree.css('div.product')
    for element in elements:
        sku = element.attributes.get('data-pid')
        image_url_raw = element.css_first('img.tile-image')
        image_url = image_url_raw.attributes.get('src')
        item_url_raw = element.css_first('a.link')
        item_url = item_url_raw.attributes.get('href')
        try:
            name_brand = tree.css_first("p.pdp-link-name.text-uppercase").text()
        except Exception as e:
            name_brand = ""

        try:
            # Selecciona el <p> con clase "pdp-link-name" que no tenga "text-uppercase"
            name_title = [p for p in element.css("p.pdp-link-name") if "text-uppercase" not in p.attributes.get("class", "")][0].text()
        except Exception as e:
            name_title = ""

        try:
            name_type = element.css_first("p.pdp-link-fragrance").text()
        except Exception as e:
            name_type = ""

        name = f'{name_brand} {name_title} {name_type}'.strip()

        try:
             pvp_raw = element.css_first('span.value')
             pvp = pvp_raw.attributes.get('content')
             sales_block = element.css_first('span.sales')
             price_raw = sales_block.css_first('span.value')
             price = price_raw.attributes.get('content')
        except Exception as e:
             pvp = None
             price_raw = element.css_first('span.value')
             price = pvp_raw.attributes.get('content')
        if pvp == price : pvp = None
        results.append({
                        "sku": sku,
                        "image_url": image_url,
                        "item_url": item_url,
                        "name": name,
                        "price": price,
                        "pvp": pvp
                    })

    with open(json_file + ".json", "w", encoding="utf-8") as f:
    
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en Aromas:", len(results))            
                