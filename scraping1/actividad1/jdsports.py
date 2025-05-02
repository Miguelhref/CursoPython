
import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.parser import HTMLParser


def scrap_jdsports(keyword, pages, json_file):
    results = []
    seen_skus = set()
    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # opts.add_argument("--headless")

    # Inicializar driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    driver.get("https://m.jdsports.es/")
    sleep(3)

    # Aceptar cookies
    try:
        cookies_button = driver.find_element(By.CLASS_NAME, "accept-all-cookies")
        cookies_button.click()
        sleep(2)

    except Exception as e:
        print("Error al aceptar las cookies:", e)

    tree = ""
    elements = []
    for i in range(0, pages):
        num_items = i * 72
        
        url = f"https://m.jdsports.es/search/{keyword}/?from={num_items}&max=72"

        driver.get(url)
        sleep(5)
        driver.execute_script("window.scrollTo(0, 1000);")
        sleep(2)
        driver.execute_script("window.scrollTo(1000, 2000);")
        sleep(2)
        driver.execute_script("window.scrollTo(2000, 3000);")
        sleep(2)
        driver.execute_script("window.scrollTo(3000, 4000);")
        
        tree = HTMLParser(driver.page_source)
        elements_raw = tree.css(".itemContainer")
        if elements_raw == None:
            break
        else:
            elements += elements_raw

    for element in elements:
        sku = element.attrs.get("data-productsku")
        img_raw = element.css_first("a.itemImage img.thumbnail")
      
        image_url = img_raw.attrs.get("src")
        item_url = "https://m.jdsports.es" + element.css_first("a.itemImage").attrs.get(
            "href"
        )

        name = img_raw.attrs.get("title")

        try:
            pvp_raw = element.css('[data-oi-price]')
            pvp = (
                pvp_raw[0]
                .text()
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
                
            )

            price_raw = element.css_first(".now")
            price = (
                pvp_raw[1]
                .text()
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
        except Exception as e:
            pvp = None

            price = (
                element.css_first(".itemPrice")
                .text()
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
                .split("-")[0]
            )

        results.append(
            {
                "sku": sku,
                "image_url": image_url,
                "item_url": item_url,
                "name": name,
                "price": float(price),
                "pvp": float(pvp) if pvp else None,
            }
        )

    with open(json_file + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Número de productos encontrados en JDSports:", len(results))
    driver.close()
    