import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrap_deporte_outlet(keyword, pages, json_file):
    results = []
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--headless")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
    
        driver.get('https://www.deporte-outlet.es/')
        sleep(3)

 
        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except:
            pass

        infinite_pages = (pages == 0)
        i = 1

        while infinite_pages or i <= pages:
            url = f'https://www.deporte-outlet.es/search?sSearch={keyword}&p={i}'
            driver.get(url)
            sleep(2)

            elements = driver.find_elements(By.CLASS_NAME, 'box--minimal')
            if not elements:
                break

            for element in elements:
                try:
                    sku = element.get_attribute('data-ordernumber')
                    image_url = element.find_element(By.TAG_NAME, 'img').get_attribute('srcset')
                    item_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    name = element.find_element(By.TAG_NAME, 'a').get_attribute('title')

                    price_int = element.find_element(By.CLASS_NAME, 'price--default-lineheight').text.replace(",", ".").replace("€", "").strip()
                    price_dec = element.find_element(By.CLASS_NAME, 'price--default-sup').text.replace(",", ".").replace("€", "").strip()
                    price = f'{price_int}{price_dec}'

                    try:
                        pvp = element.find_element(By.TAG_NAME, 'del').text.replace(",", ".").replace("€", "").strip()
                    except:
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
                    print(f"Error procesando un producto: {e}")
                    continue

            i += 1

        # Guardar resultados
        with open(json_file + ".json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("Número de productos encontrados en deporte-outlet:", len(results))

    finally:
        driver.quit()
