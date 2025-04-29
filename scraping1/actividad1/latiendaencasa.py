import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
def scrap_latiendaencasa(keyword, pages, json_file):
    results = []
    opts = Options()
    opts.add_argument("user-agent=...")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    #opts.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
        driver.get('https://www.latiendaencasa.es/')
        sleep(5)
        
        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            sleep(5)
        except:
            pass

        infinite_pages = (pages == 0)
        i = 1
        while (infinite_pages or i<=pages):

            url = f'https://www.latiendaencasa.es/search/{i}/?s={keyword}&hierarchy=&deep_search=&stype=text_box'
            driver.get(url)
            sleep(2)
            elements = driver.find_elements(By.CLASS_NAME,'obverse')
            for element in elements:
                item_url_raw = element.find_element(By.TAG_NAME,'a')
                item_url = item_url_raw.get_attribute('href')
                sku = re.search(r'/electronica/(A\d+)-', item_url)
                
                image_url = item_url_raw.find_element(By.TAG_NAME,'img').get_attribute('src')
                name = item_url_raw.get_attribute('title')
                try:
                    price = element.find_element(By.XPATH,'span[@class="price _big"]')
                except Exception as e:
                    price = element.find_element(By.XPATH,'span[@class="price _big _sale"]')

                pvp = None
                    
                results.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": price,
                    "pvp": pvp
                })
            i += 1

    except Exception as e:
        print('Error', e)

    with open(json_file + ".json", "w", encoding="utf-8") as f:
    
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en coolmod:", len(results))


    