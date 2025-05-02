'''
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrap_elcorteingles(keyword, pages, json_file):
    results = []
    seen_skus = set()
    # Opciones de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0")
    opts.add_argument("--window-position=1100,0")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--disable-http2")
    # opts.add_argument("--headless=new")

    # Inicializar driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    driver.get("https://www.elcorteingles.es/")
    sleep(3)

    # Aceptar cookies
    try:
       # Esperar hasta 10 segundos a que el botón de aceptar cookies esté disponible
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookies_button.click()
        print("Cookies aceptadas correctamente")
    except Exception as e:
        print(f"Error al aceptar las cookies: {e}")

    sleep(2)

    url = "https://www.elcorteingles.es/search-nwx/1/?s=perfume&stype=text_box"
    #url = f"https://www.elcorteingles.es/search-nwx/1/?s={keyword}&stype=text_box"
    driver.get(url)

    i = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while i <= pages or pages == 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    tree = HTMLParser(driver.page_source)
    elements = tree.css(".card")
    sleep(1)
'''
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrap_elcorteingles(keyword, pages, json_file):
    results = []
    seen_skus = set()
    
    
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    opts.add_argument("--window-size=1920,1080")  
    opts.add_argument("--disable-blink-features=AutomationControlled")  
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--disable-http2")

    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    
    
    driver.set_page_load_timeout(10)
    
    
    
    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    
    sleep(3)  # Pausa adicional
    
    cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
    cookies_button.click()
    print("Cookies aceptadas correctamente (método 1)")
     
           
        
    sleep(3)  # Pausa después de gestionar cookies
        
        
    url = f"https://www.elcorteingles.es/search-nwx/1/?s={keyword}&stype=text_box"
      
    driver.get(url)
        
       
    WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
        )
    
        
       
    i = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while i <= pages or pages == 0:
        print(f"Haciendo scroll (página {i})...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No se cargaron nuevos elementos, finalizando scroll")
            break
        last_height = new_height
        i += 1
    
        
        print("Extrayendo datos de la página...")
        tree = HTMLParser(driver.page_source)
        elements = tree.css(".card")
        print(f"Se encontraron {len(elements)} elementos con la clase .card")
        
      
        
    
    
    driver.quit()
 

