import io
import json
import time
from time import sleep
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# opts.add_argument("--headless")
diccionario = []
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

url = 'https://www.amazon.es/events/deals/?_encoding=UTF8&ref_=dealz_cs_see_more'
driver.get(url)
sleep(3)


try:
    aceptar_cookies = driver.find_element(By.XPATH, '/html/body/div[1]/span/form/div[2]/div/span[1]/span/input')
    aceptar_cookies.click()
    print("Cookies aceptadas")
    sleep(2)
except Exception:
    print("No se han mostrado cookies para aceptar")

# Set para evitar duplicados
elementos_unicos = set()
resultados = []

alto = 0
scrolls_sin_nuevos = 0

while True:
    old_count = len(elementos_unicos)
    alto += 500
    driver.execute_script(f"window.scrollTo(0, {alto});")
    sleep(1.5)

    
    tree = HTMLParser(driver.page_source)
    elementos = tree.css('div.ProductCard-module__card_uyr_Jh7WpSkPx4iEpn4w')

    for elemento in elementos:
        enlace = elemento.css_first('a[data-testid="product-card-link"]')
        href = enlace.attributes.get('href')
        if href and href not in elementos_unicos:
            elementos_unicos.add(href)
            resultados.append(href)
          

    # Detectar si ya no hay nuevos elementos
    if len(elementos_unicos) == old_count:
        scrolls_sin_nuevos += 1
    else:
        scrolls_sin_nuevos = 0

    #Clic en "Ver más"
    try:
        boton = driver.find_element(By.XPATH, '//button[contains(text(), "Ver más")]')
        boton.click()
        sleep(2)
    except Exception:
        pass

    # Detener si no hay cambios después de varios intentos
    if scrolls_sin_nuevos >= 3:
        print("No se cargan más elementos nuevos.")
        break
for resultado in resultados:
    driver.get(resultado)
    item_url = resultado
    tree = HTMLParser(driver.page_source)

    
    name_element = tree.css_first('#productTitle')
    name = name_element.text().strip() if name_element else None

    
    precio_oferta_element = tree.css_first('span.a-price span.a-offscreen')
    price =  precio_oferta_element.text().strip().replace(".", "").replace(",", ".").replace("€", "")
    
    pvp = None
    try:
       
        for span in tree.css('span.a-price.a-text-price'):
            parent_text = span.parent.text(strip=True)
            if "Precio recomendado" in parent_text:
                offscreen = span.css_first('span.a-offscreen')
                if offscreen:
                    pvp = offscreen.text().strip().replace(".", "").replace(",", ".").replace("€", "")
                    break  
    except Exception as e:
        print(f"Error extrayendo el PVP para {item_url}: {e}")

    imagen_element = tree.css_first('#imgTagWrapperId img')
    image_url = imagen_element.attributes.get('src') if imagen_element else None
    asin_div = tree.css_first('div#averageCustomerReviews')
    sku = asin_div.attributes.get('data-asin')
    
   
# Si hay solo uno y es el del ASIN, puedes tomarlo directamente
    
    diccionario.append(
                    {"sku":sku,
                    "image_url":image_url,
                    "item_url":item_url,
                    "name":name,
                    "price":price,
                    "pvp":pvp
                    })
print(f"\nTotal elementos únicos encontrados: {len(resultados)}")
for i, url_elemento in enumerate(resultados):
    print(f"\n Elemento {i+1}:\n{url_elemento}")

try: 
    
    diccionario_json = json.dumps(diccionario)
    print(diccionario_json)
    with io.open("amazon_ofertas.json","w",encoding="utf-8") as file:
        json.dump(diccionario,file,ensure_ascii=False)
        tiempo_final= time.time()
except json.JSONDecodeError as e:
    print("Error codificando JSON:",str(e))

print("Numero de items recogidos:",len(diccionario))
driver.quit()
