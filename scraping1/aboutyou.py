import io
import json
import time
from time import sleep
import requests
from selectolax.parser import HTMLParser
import selectolax
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import re

def scrap_jack_jones(keyword, pages, json_file):
    #terminaciones de urls por categoria dentro de las marcas
    mujer = '20201'
    hombre = '20202'
    infantil = '138113'

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    opts.add_argument("--headless")

    diccionario = [] #para guardar los resultados

    #driver principal
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    #driver de pruebas para coger marca y titulo
    driver_test = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver.get('https://www.aboutyou.es/')
    sleep(3)


    with requests.Session() as session:
        
        response = session.get('https://www.aboutyou.es/')

    try:
        url = 'https://www.aboutyou.es/marca?category=20201'
        #url = 'https://www.aboutyou.es'
        driver.get(url)
        
        #le paso a selectlax el html conseguido con selenium
        tree = HTMLParser(driver.page_source)

        marcas=[]
        limite_pruebas = 0

        #guardo en una lista el listado de marcas de la web
        for link in tree.css('a[data-testid="LinkToUrl"]'):
            
            if limite_pruebas <3:
                href = link.attributes.get('href')
                marcas.append('https://www.aboutyou.es'+href)

                #compruebo si esa marca tiene seccion de hombre e infantil
                url_hombre = ('https://www.aboutyou.es'+href).replace('20201',hombre)
                driver_test.get(url_hombre)
                sleep(1)
                if driver_test.current_url == url_hombre:
                    marcas.append(url_hombre)
                url_infantil = ('https://www.aboutyou.es'+href).replace('20201',infantil)
                driver_test.get(url_infantil)
                sleep(1)
                if driver_test.current_url == url_infantil:
                    marcas.append(url_infantil)
                
                limite_pruebas+=1
            else:
                break
        print(marcas)

        for marca in marcas:
            url = marca
            
            driver.get(url)
            while True:
                #hago scroll infinito hasta el final para obtener todo el html
                old_height = driver.execute_script("return document.body.scrollHeight")

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                sleep(1)

                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == old_height:

                    break
            print(response.status_code)
            tree = HTMLParser(driver.page_source)
            elementos = tree.css("div.pxkk8hk")
            for elemento in elementos:
                contador = 0
                enlace_node = elemento.css_first('a')
                if enlace_node:
                    enlace = 'https://www.aboutyou.es'+enlace_node.attributes.get('href').strip()
                    print("Enlace",enlace)
                
                
                #match = re.search(r'/p/([^/]+)/([^/]+)-\d+$', enlace)

                #cojo marca y nombre del articulo
                driver_test.get(enlace)
                tree = HTMLParser(driver_test.page_source)
                sleep(1)
                titulo = tree.css_first('h1[data-testid="productName"]').text()
                print(titulo)
                '''if match:
                    marca = match.group(1).upper()        
                    nombre_raw = match.group(2)           
                    nombre = nombre_raw.replace('-', ' ')
                    nombre = ' '.join(word for word in nombre_raw.split('-'))
                    nombre = nombre[0].upper() + nombre[1:]
                    titulo = f"{marca} {nombre}"
                    print(titulo)
                else:
                    print("No habia coincidencia en el patron")
                '''
                #cojo el precio y los separo en precio oferta y habitual (si tiene los 2)
                precio = elemento.css_first("div.wq8d8k7")
                
                precio = precio.text()
            
                match_precio = re.search(r'(\d+,\d{2}) €(\d+,\d{2})', precio)
                if match_precio:
                    precio_oferta= (match_precio.group(1).strip()+"€").replace(",",".")
                    precio_habitual= (match_precio.group(2).strip()+"€").replace(",",".")
                
                    print("Precio oferta:",precio_oferta)
                    print("Precio habitual:",precio_habitual)
                else:
                    precio_oferta= precio.replace(" ","").replace(",",".")
                    precio_habitual=""
                    #precio_oferta= match_precio.group(1).strip()+"€"
                    print("Precio oferta:",precio_oferta)
                imagen_node_div = elemento.css_first('div.pxkk8hk')
                imagen_node = imagen_node_div.css_first("img")
                imagen = imagen_node.attributes.get("srcset").split("?")[0]
                
                print("Imagen:",imagen)
                diccionario.append(
                        {"Titulo":titulo,
                        "Enlace":enlace,
                        "Precio oferta":precio_oferta,
                        "Precio habitual":precio_habitual,
                        "Imagen":imagen
                        })
    except Exception as e:

        print(response.status_code)
        print(e)
    try: 
        
        diccionario_json = json.dumps(diccionario)
        print(diccionario_json)
        with io.open("about_you.json","w",encoding="utf-8") as file:
            json.dump(diccionario,file,ensure_ascii=False)
            tiempo_final= time.time()
    except json.JSONDecodeError as e:
        print("Error codificando JSON:",str(e))

    print("Numero de items recogidos:",len(diccionario))