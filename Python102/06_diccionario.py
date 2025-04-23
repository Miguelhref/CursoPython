import random

paises = ['col','mex','bol','pe']
poblacion_v2 = { pais: random.randint(1,100) for pais in paises}
print(poblacion_v2)

result = {pais:poblacion for (pais, poblacion) in poblacion_v2.items() if poblacion > 20 }
print(result)

text = 'Hola, soy BlaBla'
unique = { c: c.upper() for c in text if c in 'aeiou'}
print(unique)