#import carrefour #falta acabar
from lefties import scrap_lefties
from pullandbear import scrap_pullandbear
from glisshop import scrap_glisshop
from electroprecio import scrap_electroprecio
import threading
keyword = 'televisor'

#carrefour.search(keyword)
#scrap_lefties(archivo_json="sudaderas_lefties",keyword=keyword)
#scrap_pullandbear(archivo_json="sudaderas_pullandbear",keyword=keyword)
# Funciones de scraping
def run_glisshop():
    scrap_glisshop(keyword, 3, f"{keyword}_glisshop")

def run_electroprecio():
    scrap_electroprecio(keyword, 3, f"{keyword}_electroprecio")

# Crear los hilos
threads = [
    threading.Thread(target=run_glisshop),
    threading.Thread(target=run_electroprecio),
]

#iniciar los hilos
for t in threads:
    t.start()

#terminar los hilos
for t in threads:
    t.join()