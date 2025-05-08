# import carrefour #falta acabar
# from fnac import scrap_fnac
##### FALTA DOSFARMA, TIENE CAPTCHA
##### latiendaencasa()), acabar, fallaba la conexion
##### alcampo()), acabar, casi rehacer de 0
##### elcorteingles, falta acabar, no me carga bien la url despues de buscar
##JDSPorts no carga a tiempo las imagenes
####Falta FNAC, Me bloquea todo el rato

# TOKEN_BBDD= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnRydWUsImlhdCI6MTc0NjY5MTM5MS42NjU5OTJ9.gebJCnB2mDIY9McfocdH4Z-m7--NfxDeP4AfewPDOi0"
from lefties import scrap_lefties
from pullandbear import scrap_pullandbear
from glisshop import scrap_glisshop
from electroprecio import scrap_electroprecio
from deporte_outlet import scrap_deporte_outlet
from coolmod import scrap_coolmod
from latiendaencasa import scrap_latiendaencasa
from alcampo import scrap_alcampo
from aromas import scrap_aromas
from electrodepot import scrap_electrodepot
from alltricks import scrap_alltricks
from lookfantastic import scrap_lookfantastic
from atida import scrap_atida
from decathlon import scrap_decathlon
from alternate import scrap_alternate
from douglas import scrap_douglas
from elcorteingles import scrap_elcorteingles
from jdsports import scrap_jdsports
from jack_jones import scrap_jack_jones
from about_you import scrap_aboutyou
from euronics import scrap_euronics
from hp import scrap_hp
from ldlc import scrap_ldlc

import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.repository.Keyword import KeywordRepo


import threading


while True:
    keywords = KeywordRepo.get_by_store_id()

    """
    # Funciones de scraping
    def run_glisshop():
        scrap_glisshop(keyword, pages, f"{keyword}_glisshop")

    def run_electroprecio():
        scrap_electroprecio(keyword, pages, f"{keyword}_electroprecio")

    def run_deporte_outlet():
        scrap_deporte_outlet(keyword, pages, f"{keyword}_deporte_outlet")

    def run_coolmod():
        scrap_coolmod(keyword, pages, f"{keyword}_coolmod")

    def run_latiendaencasa():
        scrap_latiendaencasa(keyword, pages, f"{keyword}_latiendaencasa")

    def run_alcampo():
        scrap_alcampo(keyword, pages, f"{keyword}_alcampo")

    def run_aromas():
        scrap_aromas(keyword, pages, f"{keyword}_aromas")

    def run_electrodepot():
        scrap_electrodepot(keyword, pages, f"{keyword}_electrodepot")

    def run_alltricks():
        scrap_alltricks(keyword, pages, f"{keyword}_alltricks")

    def run_lookfantastic():
        scrap_lookfantastic(keyword, pages, f"{keyword}_lookfantastic")

    def run_atida():
        scrap_atida(keyword, pages, f"{keyword}_atida")

    def run_decathlon():
        scrap_decathlon(keyword, pages, f"{keyword}_decathlon")

    def run_alternate():
        scrap_alternate(keyword, pages, f"{keyword}_alternate")

    def run_douglas():
        scrap_douglas(keyword, pages, f"{keyword}_douglas")

    def run_elcorteingles():
        scrap_elcorteingles(keyword, pages, f"{keyword}_elcorteingles")

    def run_jdsports():
        scrap_jdsports(keyword, pages, f"{keyword}_jdsports")


    def run_jack_jones():
        scrap_jack_jones(keyword, 0, f"{keyword}_jack_jones")

    def run_about_you():
        scrap_aboutyou(keyword, 3, f"{keyword}_aboutyou")

    def run_euronics():
        scrap_euronics(keyword, 3, f"{keyword}_euronics")

    #def run_hp():
        #   scrap_hp(keyword, 3,f"{keyword}_hp")

    

    def run_ldlc():
        
        scrap_ldlc(keyword, 3, f"{keyword}_ldlc")
    """

    def run_hp():
        scrap_hp()

    # Crear los hilos
    threads = [
        # threading.Thread(target=run_glisshop), revisar
        # threading.Thread(target=run_electroprecio), revisar
        # threading.Thread(target=run_deporte_outlet),
        # threading.Thread(target=run_coolmod),
        # threading.Thread(target=run_latiendaencasa), acabar, fallaba la conexion
        # threading.Thread(target=run_alcampo), acabar, casi rehacer de 0
        # threading.Thread(target=run_aromas)
        # threading.Thread(target=run_electrodepot)
        # threading.Thread(target=run_alltricks)
        # threading.Thread(target=run_lookfantastic)
        #  threading.Thread(target=run_atida)
        #  threading.Thread(target=run_decathlon)
        #  threading.Thread(target=run_alternate)
        # threading.Thread(target=run_douglas)
        # threading.Thread(target=run_elcorteingles)
        # threading.Thread(target=run_jdsports)
        # threading.Thread(target=run_fnac)
        # threading.Thread(target=run_jack_jones)
        # threading.Thread(target=run_about_you)
        # threading.Thread(target=run_euronics)
        threading.Thread(target=run_hp)
        # threading.Thread(target=run_ldlc)
        #
    ]

    # iniciar los hilos
    for t in threads:
        t.start()

    # terminar los hilos
    for t in threads:
        t.join()
