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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrap_pullandbear(keyword,archivo_json):
    diccionario = []


    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (...) Safari/537.36")
    opts.add_argument("--window-position=1100,0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    driver.get("https://www.pullandbear.com/es/")
    sleep(3)

    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    for i in range(1, 3):
        if i == 1:
            driver.get(f"https://www.pullandbear.com/es/?q={keyword}&filter=hierarchical_category%3A1030574249&page=1")
        else:
            sleep(3)
            driver.get(f"https://www.pullandbear.com/es/?q={keyword}&filter=hierarchical_category%3A1030575241&page=1")

        sleep(3)

        url_anterior = None
        while url_anterior != driver.current_url:
            url_anterior = driver.current_url
            search_app = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'search-app')))
            search_app_shadow = driver.execute_script('return arguments[0].shadowRoot', search_app)
            search_grid = search_app_shadow.find_element(By.CSS_SELECTOR, 'search-grid')
            search_grid_shadow = driver.execute_script('return arguments[0].shadowRoot', search_grid)

            scroll_container = search_grid_shadow.find_element(By.CSS_SELECTOR, 'section.grid-area.hide-scroll-bar')
            sleep(1)
            scroll_container.send_keys(Keys.END)
            sleep(3)

        productos = search_grid_shadow.find_elements(By.CSS_SELECTOR, 'grid-product')

        for producto in productos:
            try:
                product_shadow = driver.execute_script('return arguments[0].shadowRoot', producto)
                article = product_shadow.find_element(By.CSS_SELECTOR, 'article')
                link_elem = article.find_element(By.CSS_SELECTOR, 'a')
                item_url = link_elem.get_attribute("href")
                name = link_elem.get_attribute("title")

                try:
                    color_selector = article.find_element(By.CSS_SELECTOR, 'product-color-selector')
                    sku = color_selector.get_attribute('product-id')
                except NoSuchElementException:
                    sku = None

                # Obtener imagen (video o imagen estática)
                image_url = None
                try:
                    x_media = link_elem.find_element(By.CSS_SELECTOR, 'x-media')
                    x_media_shadow = driver.execute_script('return arguments[0].shadowRoot', x_media)

                    try:
                        video_element = x_media_shadow.find_element(By.CSS_SELECTOR, 'video-element')
                        video_shadow = driver.execute_script('return arguments[0].shadowRoot', video_element)
                        video_tag = video_shadow.find_element(By.CSS_SELECTOR, 'video')
                        image_url = video_tag.get_attribute("poster")
                    except NoSuchElementException:
                        try:
                            lazy_image = x_media_shadow.find_element(By.CSS_SELECTOR, 'lazy-image')
                            lazy_image_shadow = driver.execute_script('return arguments[0].shadowRoot', lazy_image)
                            img_tag = lazy_image_shadow.find_element(By.CSS_SELECTOR, 'img#image')
                            image_url = img_tag.get_attribute("src")
                        except NoSuchElementException:
                            print(f"No se encontró imagen ni video en: {name}")
                except Exception as e:
                    print(f"No se pudo obtener imagen: {e}")
                    print("Error al obtener la imagen de:", name)
                    image_url = None
                    continue

                # Obtener precio
                try:
                    price_elem = article.find_element(By.CSS_SELECTOR, 'price-element')
                    price_shadow = driver.execute_script("return arguments[0].shadowRoot", price_elem)
                    price = price_shadow.find_element(By.CSS_SELECTOR, 'p.sale.price').text.replace("\xa0", "").replace(",", ".").strip()
                    pvp = price_shadow.find_element(By.CSS_SELECTOR, 'p.old.price').text.replace("\xa0", "").replace(",", ".").strip()
                except NoSuchElementException:
                    price_elem = article.find_element(By.CSS_SELECTOR, 'price-element')
                    price_shadow = driver.execute_script("return arguments[0].shadowRoot", price_elem)
                    price = price_shadow.find_element(By.CSS_SELECTOR, 'p.price').text.replace("\xa0", "").replace(",", ".").strip()
                    pvp = None

                diccionario.append({
                    "sku": sku,
                    "image_url": image_url,
                    "item_url": item_url,
                    "name": name,
                    "price": price,
                    "pvp": pvp
                })

            except Exception as e:
                print("Error procesando producto:", e)

    # Guardar resultados
    with open(archivo_json + ".json", "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)

    print("Numero de productos encontrados:",len(diccionario))
    driver.quit()
