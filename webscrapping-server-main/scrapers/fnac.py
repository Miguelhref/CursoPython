import random
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Inicializar resultados y conjunto de SKUs vistos
results = []
seen_skus = set()

# Configuración de opciones para Chrome
options = uc.ChromeOptions()  # Usamos uc.ChromeOptions() de undetected_chromedriver
options.add_argument("user-agent=Mozilla/5.0")  # User-Agent básico (puedes mejorarlo)
options.add_argument("--window-position=1100,0")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--headless")  # Ejecuta el navegador sin interfaz gráfica (opcional)
options.add_argument("--disable-gpu")  # Desactiva la GPU para mejorar el rendimiento

# Configura el User-Agent como Google Chrome
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)
#options.add_argument(f"user-agent={user_agent}")

# Inicializa el driver con las opciones configuradas
driver = uc.Chrome(options=options)

# Accede a la página principal de FNAC
driver.get("https://www.fnac.es/")

# Espera aleatoria de 3 a 5 segundos para simular comportamiento humano
sleep(random.uniform(3, 5))

# Intenta aceptar cookies si el botón está disponible
try:
    cookies_button = driver.find_element(By.CLASS_NAME, "onetrust-accept-btn-handler")
    cookies_button.click()
    sleep(random.uniform(2, 4))
except Exception as e:
    print('Error al aceptar las cookies:', e)

# Aquí puedes agregar la lógica para realizar el scraping, por ejemplo:
# print(driver.title)  # Solo para probar si llegamos correctamente

# Cierra el navegador
driver.quit()
