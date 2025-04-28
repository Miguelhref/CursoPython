import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
def scrap_coolmod(keyword, pages, json_file):
    results = []
    seen_skus = set()  # <--- nuevo
    opts = Options()
    opts.add_argument("user-agent=...")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
        driver.get('https://www.coolmod.com/')
        sleep(3)
        
        try:
            driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
            sleep(5)
        except:
            pass

        infinite_pages = (pages == 0)
        i = 1
        while (infinite_pages or i<=pages):

            url = f'http://coolmod.com/#01cc/fullscreen/m=and&p={i}&q={keyword}'
            driver.get(url)
            sleep(2)
            elements = driver.find_elements(By.CLASS_NAME,'dfd-card-preset-product')
            for element in elements:
                image_url = element.find_element(By.TAG_NAME,'img').get_attribute('src')
                
                sku_raw = element.find_element(By.CLASS_NAME,'dfd-cart-add-button')
                sku_button = sku_raw.find_element(By.TAG_NAME,'button')
                sku_raw_attr = sku_button.get_attribute('data-item')
                sku_match = re.search(r'PROD-(\d+)', sku_raw_attr)
                
                sku = sku_match.group(1)
                
                if sku in seen_skus:
                    continue  # <--- no guardar duplicados
                seen_skus.add(sku)

                item_url = element.find_element(By.TAG_NAME,'a').get_attribute('href')
                name = element.find_element(By.CLASS_NAME,'dfd-card-title').get_attribute('title')
                try:
                    element_price = element.find_element(By.CLASS_NAME,'dfd-card-pricing')
                    pvp = element_price.find_elements(By.CLASS_NAME,'dfd-card-price')[1].text.replace(".","").replace(",",".").replace("€","")
                    price = element_price.find_element(By.CLASS_NAME,'dfd-card-price--sale').text.replace(".","").replace(",",".").replace("€","")
                except Exception:
                    element_price = element.find_element(By.CLASS_NAME,'dfd-card-pricing')
                    price = element_price.find_element(By.CLASS_NAME,'dfd-card-price').text.replace(".","").replace(",",".").replace("€","")
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