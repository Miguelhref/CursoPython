import io
import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
diccionario = []
def scrap_lefties(keyword,archivo_json):
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    opts.add_argument("--window-position=1100,0")
    opts.add_argument("--headless")
    diccionario = []
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )


    url = 'https://www.lefties.com/es/'
    driver.get(url)
    sleep(2)

    boton_cookies = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    boton_cookies.click()

    



    driver.get(f"https://www.lefties.com/es/?query={keyword}")
    url_anterior = None
    url_nueva = driver.current_url
    while (url_anterior!= url_nueva):
        url_anterior=driver.current_url
        scroll_container = driver.find_element(By.ID,'lft-search')
        scroll_container.send_keys(Keys.END)
        sleep(3)
        url_nueva= driver.current_url
        sleep(1)




    elementos = driver.find_elements(By.CLASS_NAME,'lft-grid-product')
    num_elementos = len(elementos)
    try:
        intentos =0
        for elemento in elementos:
            sku = elemento.get_attribute("data-mocaid")
            image_raw = elemento.find_element(By.CLASS_NAME,"grid-product-image")
            image_url = image_raw.get_attribute('src')
            item_url = elemento.get_attribute('href')
            name = elemento.find_element(By.CLASS_NAME,'name').text
            price = elemento.find_element(By.CLASS_NAME,'price').text.replace(".","").replace(",",".").replace("€","").strip()
            pvp= None
            diccionario.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": float(price),
                    "pvp": float(pvp) if pvp else None
                    })
            
    except Exception as e:
        if intentos <4:
            sleep(10)
            intentos+=1
        else:
            print("se ha llegado al limite de intentos")
            print(e)
            pass
    try: 
        
        diccionario_json = json.dumps(diccionario)
        print(diccionario_json)
        with io.open(f"{archivo_json}.json","w",encoding="utf-8") as file:
            json.dump(diccionario,file,ensure_ascii=False)
            
    except json.JSONDecodeError as e:
        print("Error codificando JSON:",str(e))

    print("Numero de items recogidos en lefties para la palabra :",keyword,len(diccionario))
    driver.quit()

