#import carrefour #falta acabar
from lefties import scrap_lefties
from pullandbear import scrap_pullandbear
from glisshop import scrap_glisshop
keyword = 'sudadera'

#carrefour.search(keyword)
#scrap_lefties(archivo_json="sudaderas_lefties",keyword=keyword)
#scrap_pullandbear(archivo_json="sudaderas_pullandbear",keyword=keyword)
scrap_glisshop('gafas',3,"gafas_glishop")
