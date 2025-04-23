from time import sleep
import requests
from selectolax.parser import HTMLParser
import selectolax
with requests.Session() as session:
    
#response = session.get('https://www.euronics.es/')

#profile = session.get('https://www.euronics.es/lavadora-carga-frontal.html')

    url = 'https://www.euronics.es/'
response = requests.get(url)
print(response.status_code)
tree = HTMLParser(response.content)


lista_mas_buscados = []

for link in tree.css('.linkscategorieshome a'):
    href = link.attributes.get('href')
    if href and href.startswith('http'):
        lista_mas_buscados.append(href)


print(lista_mas_buscados)
for direccion in lista_mas_buscados:
    try:
        html = requests.get(direccion)
        print(html.status_code)
        tree = HTMLParser(html.content)
        sleep(5)


        elementos = tree.css('li')
        for elemento in elementos:
            contador = 0
            titulo_node = elemento.css_first('h2 > a') 
            precio_node = elemento.css_first('div.precioProducto')
            imagen_node = elemento.css_first('div.imagen img')
            
            if titulo_node :
                titulo = titulo_node.text().strip()
                precio = precio_node.text().strip() 
                imagen = imagen_node.attributes.get('src').strip() 
                enlace = "https://www.euronics.es"+titulo_node.attributes.get('href').strip()
                print("Titulo:", titulo) 
                print("Precio:", precio)
                print("Imagen:", imagen)
                print("Enlace:",enlace)
            else:
                continue
    except Exception as e:
                print("Error con estado:",html.status_code)
                print(e)
                contador+=1

                if contador<4:
                    print("Sleep de 15 secs y reintentando")
                    sleep(15)
                    continue    

    