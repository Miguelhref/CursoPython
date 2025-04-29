#import carrefour #falta acabar
from lefties import scrap_lefties
from pullandbear import scrap_pullandbear
from glisshop import scrap_glisshop
from electroprecio import scrap_electroprecio
from deporte_outlet import scrap_deporte_outlet
from coolmod import scrap_coolmod
from latiendaencasa import scrap_latiendaencasa
import threading

keyword = 'tv'

#carrefour.search(keyword)
#scrap_lefties(archivo_json="sudaderas_lefties",keyword=keyword)
#scrap_pullandbear(archivo_json="sudaderas_pullandbear",keyword=keyword)
# Funciones de scraping
def run_glisshop():
    scrap_glisshop(keyword, 3, f"{keyword}_glisshop")

def run_electroprecio():
    scrap_electroprecio(keyword, 3, f"{keyword}_electroprecio")

def run_deporte_outlet():
    scrap_deporte_outlet(keyword, 3, f"{keyword}_deporte_outlet")

def run_coolmod():
    scrap_coolmod(keyword, 3, f"{keyword}_coolmod")

def run_latiendaencasa():
    scrap_latiendaencasa(keyword, 3, f"{keyword}_latiendaencasa")
# Crear los hilos
threads = [
   # threading.Thread(target=run_glisshop), revisar
   # threading.Thread(target=run_electroprecio), revisar
   # threading.Thread(target=run_deporte_outlet),
   # threading.Thread(target=run_coolmod()),
   # threading.Thread(target=run_latiendaencasa()), acabar, fallaba la conexion
]

#iniciar los hilos
for t in threads:
    t.start()

#terminar los hilos
for t in threads:
    t.join()