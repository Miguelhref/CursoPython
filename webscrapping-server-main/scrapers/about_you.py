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

def scrap_aboutyou(keyword, pages, json_file):
    results = []
    seen_skus = set()

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.aboutyou.es")
    sleep(3)

    # Aceptar cookies
    try:
        shadow_host = driver.find_element(By.CSS_SELECTOR, "#usercentrics-cmp-ui")
        shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
        accept_button = shadow_root.find_element(By.CSS_SELECTOR, 'button[data-action-type="accept"]')
        accept_button.click()
        sleep(2)
    except Exception as e:
        print("Error al aceptar las cookies:", e)

    urls = [
        "https://www.aboutyou.es/?gender=female",
        "https://www.aboutyou.es/?gender=male",
        "https://www.aboutyou.es/c/infantil-138113"
    ]

    for url in urls:
        try:
            driver.get(url)
            sleep(2)

            try:
                search_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="searchIcon"]')
                search_icon.click()
                sleep(1)
            except:
                pass

            search_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="searchBarInput"]')
            search_input.click()
            search_input.clear()
            search_input.send_keys(keyword)
            sleep(2)
            search_input.send_keys(Keys.RETURN)
            sleep(3)

            # Scroll dinámico dentro del contenedor con data-testid="sectionEnd"
            last_height = 0
            same_count = 0
            for scroll in range(pages):
                try:
                    scroll_container = driver.find_element(By.CSS_SELECTOR, '[data-testid="sectionEnd"]')
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", scroll_container)
                    sleep(2)    

                    current_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

                    if current_height == last_height:
                        same_count += 1
                        if same_count >= 2:
                            break
                    else:
                        same_count = 0
                        last_height = current_height
                except Exception as e:
                    print(f"No se pudo hacer scroll: {e}")
                    break

            # Parsear HTML sin recargar
            tree = HTMLParser(driver.page_source)
            elements = tree.css('[data-testid^="productTileTracker-"]')

            for element in elements:
                try:
                    sku_raw = element.attrs.get('data-testid', '')
                    sku_match = re.search(r'\d+$', sku_raw)
                    if not sku_match:
                        continue
                    sku = sku_match.group(0)

                    if sku in seen_skus:
                        continue

                    seen_skus.add(sku)

                    img = element.css_first('img')
                    name = img.attrs.get('alt') if img else None
                    image_url = img.attrs.get('src') if img else None

                    a_tag = element.css_first('a')
                    item_url = 'https://www.aboutyou.es' + a_tag.attrs.get('href') if a_tag else None

                    # Extraer y limpiar precio
                    price_tag = element.css_first('span[data-testid="finalPrice"]') or element.css_first('span[data-testid="from-price"]')
                    price = None
                    if price_tag:
                        price_text = price_tag.text()
                        price_text_clean = re.sub(r"[^\d,\.]", "", price_text)
                        price_text_clean = price_text_clean.replace('.', '').replace(',', '.').strip()
                        price = float(price_text_clean) if price_text_clean else None

                    # Extraer y limpiar PVP
                    pvp_tag = element.css_first('span[data-testid="StruckPrice"]')
                    pvp = None
                    if pvp_tag:
                        pvp_text = pvp_tag.text()
                        pvp_text_clean = re.sub(r"[^\d,\.]", "", pvp_text)
                        pvp_text_clean = pvp_text_clean.replace('.', '').replace(',', '.').strip()
                        pvp = float(pvp_text_clean) if pvp_text_clean else None

                    results.append({
                        "sku": sku,
                        "image_url": image_url,
                        "item_url": item_url,
                        "name": name,
                        "price": price,
                        "pvp": pvp
                    })

                except Exception as e:
                    print(f"Error al procesar elemento: {e}")

        except Exception as e:
            print(f"Error general: {e}")

    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos únicos encontrados en AboutYou:", len(results))
    driver.quit()
