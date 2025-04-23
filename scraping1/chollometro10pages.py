import json
import io
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
opts.add_argument("--headless")

diccionario = []
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)
for i in range (1,11):

   
    driver.get(f'https://www.chollometro.com/?page={i}')

    sleep(3)
    if i==1:
        try:
            aceptar_cookies = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[4]/div[3]/div[2]/div/section/div/div/div/div/div/div[2]/div[3]/div/button[1]')
        except Exception as e:
            print("no se ha podido aceptar las cookies")
        aceptar_cookies.click()
        print("cookies aceptadas")
        sleep(3)
    
    elements = driver.find_elements(By.XPATH,"//div[@class='threadListCard thread-clickRoot']")
   

    print("Imprimiento titulos")

    for element in elements:

        try:
            tag_imagen = element.find_element(By.XPATH,".//img")
            imagen = tag_imagen.get_attribute("src")
            a_tag = element.find_element(By.XPATH, ".//a")
            titulo = a_tag.get_attribute("title") 
            enlace = a_tag.get_attribute("href")
        
            precio_oferta = element.find_element(
                By.XPATH, ".//span[contains(@class, 'thread-price')]"
            ).text
                
            if "K" in precio_oferta:
                precio_oferta = precio_oferta.replace("K","").replace("€","").strip()
                precio_oferta = float(precio_oferta) * 1000
                
                if precio_oferta.is_integer():
                    precio_oferta = str(int(precio_oferta))+"€"
                else:
                    precio_oferta = str(precio_oferta)+"€"
            
            
        
            try:
                precio_habitual = element.find_element(
                By.XPATH,".//span[contains(@class, 'color--text-NeutralSecondary') and contains(@class, 'text--lineThrough')]"
                ).text
            
                if "K" in precio_habitual:
                    precio_habitual = precio_habitual.replace("K","").replace("€","").strip()
                    precio_habitual = float(precio_habitual) * 1000
                    
                    if precio_habitual.is_integer():
                        precio_habitual = str(int(precio_habitual))+"€"
                    else:
                        precio_habitual = str(precio_habitual)+"€"
            except Exception as e:  
                precio_habitual= ""
                    
            precio_oferta= precio_oferta.replace(",",".")
            precio_habitual= precio_habitual.replace(",",".")
            print(f"Título: {titulo}")
            
            print(f"Enlace: {enlace}")
            
            print(f"Precio oferta: {precio_oferta}")
           
            print(f"Precio habitual: {precio_habitual}")
            

            print(f"Imagen: {imagen}")
           
            print("-------------------------------------------")
            diccionario.append(
                {"Titulo":titulo,
                 "Enlace":enlace,
                 "Precio oferta":precio_oferta,
                 "Precio habitual":precio_habitual,
                 "Imagen":imagen
                 })
        except Exception as e:
            pass
    
try: 
    diccionario_json = json.dumps(diccionario)
    print(diccionario_json)
    with io.open("chollometro10pages.json","w",encoding="utf-8") as file:
        json.dump(diccionario,file,ensure_ascii=False)
except json.JSONDecodeError as e:
    print("Error codificando JSON:",str(e))
