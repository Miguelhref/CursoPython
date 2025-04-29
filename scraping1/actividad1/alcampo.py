import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrap_alcampo(keyword, pages, json_file):
    results = []
    seen_skus = set()  # Guardamos las SKU ya vistas

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    # opts.add_argument("--headless")  # opcional

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
        driver.get('https://www.alcampo.es/')
        sleep(5)

        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            sleep(3)
        except:
            pass

        infinite_pages = (pages == 0)
        url = f'https://www.compraonline.alcampo.es/search?q={keyword}'
        driver.get(url)
        sleep(4)

        i = 1
        while infinite_pages or i <= pages:
            # Recolectar productos visibles
            elements = driver.find_elements(By.CLASS_NAME, 'product-card-container')
            for element in elements:
                try:
                    a_tag = element.find_element(By.CSS_SELECTOR, 'a')
                    item_url = a_tag.get_attribute('href')
                    sku_match = re.search(r'/(\d+)$', item_url)
                    if not sku_match:
                        continue
                    sku = sku_match.group(1)

                    if sku in seen_skus:
                        continue  # Ya procesado
                    seen_skus.add(sku)

                    name = a_tag.get_attribute('aria-label')
                    image_url = element.find_element(By.TAG_NAME, 'img').get_attribute('src')

                    try:
                        pvp = element.find_element(By.XPATH, './/span[@data-test="fop-original-price"]').text
                    except:
                        pvp = None
                    try:
                        price = element.find_element(By.XPATH, './/span[@data-test="fop-price"]').text
                    except:
                        price = ''

                    results.append({
                        "sku": sku,
                        "image_url": image_url,
                        "item_url": item_url,
                        "name": name,
                        "price": price,
                        "pvp": pvp
                    })
                except Exception as e:
                    print("❌ Error en producto:", e)

            # Scroll
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == old_height:
                break
            i += 1

    except Exception as e:
        print("❌ Error general:", e)
    finally:
        driver.quit()

    # Guardar resultados
    try:
        with open(json_file + ".json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(results)} productos guardados en {json_file}.json")
    except Exception as e:
        print("❌ Error al guardar JSON:", e)
