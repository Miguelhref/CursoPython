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


def scrap_hp(keyword, pages, json_file):
    results = []
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--headless")  
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.hp.es")
    sleep(3)

    # Aceptar cookies
    try:
        
        accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_button.click()
        sleep(2)
    except Exception as e:
        print('Error al aceptar las cookies')
    
    ###No voy a poner limite de paginas, ya que HP tiene en total 2300 productos y las categorias mas largas andan en unos 100,
    ### así que mostraré todos los productos de la busqyeda usando el boton de mostrar TODOS (para esa busqueda) en la web

    url = f'https://www.hp.com/es-es/shop/list.aspx?fc_ptyp_printers=1&sel=prn&q={keyword}'
    driver.get(url)
    sleep(2)
    button_all = driver.find_element(By.XPATH,'//button[@aria-label="Todos"]').click()
    #driver.get(driver.current_url)
    sleep(2)
    tree = HTMLParser(driver.page_source)

    elements = tree.css('.HorizontalProductTile_container__3F4IN')

    for element in elements:
        try:
            item_url = element.css_first('a').attrs.get('href') #esto da https://www.hp.com/es-es/shop/product.aspx?id=588R4B&opt=629&sel=PRN
            image_url = element.css_first('img').attrs.get('src')
            
            name = name = element.css_first('a span p').text().strip()
            sku = re.search(r'id=([^&]+)', item_url).group(1)
            try:
                pvp = element.css_first('span[data-test-hook="@hpstellar/core/price-block__strike-price"]').text().replace(' ','').replace('.','').replace(',','.').replace('€','')
                price =  element.css_first('div[data-test-hook="@hpstellar/core/price-block__sale-price"]').text().replace(' ','').replace('.','').replace(',','.').replace('€','')
            except Exception as e:
                price =  element.css_first('div[data-test-hook="@hpstellar/core/price-block__sale-price"]').text().replace(' ','').replace('.','').replace(',','.').replace('€','')
                pvp = None
            results.append({
                            "sku": sku,
                            "image_url": image_url,
                            "item_url": item_url,
                            "name": name,
                            "price": float(price),
                            "pvp": float(pvp) if pvp else None
                        })
        except Exception as e:
            continue
    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en hp:", len(results))
    driver.quit()