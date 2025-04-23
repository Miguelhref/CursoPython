'''
diccionario = {}
for i in range(1,11):
    diccionario[i] = i*2

print(diccionario)

diccionario_v2 = {i: i * 2 for i in range(1,11) }
print(diccionario_v2)
'''
'''
import random
paises = ['col','mex','bol','pe']
poblacion = {}
for pais in paises:
    poblacion[pais] = random.randint(1,100) 

print(poblacion)

poblacion_v2 = { pais: random.randint(1,100) for pais in paises}
print(poblacion_v2)
'''

nombres = ['nico','zule','santi']
edades = [12,56,98]

print(list(zip(nombres,edades)))

nuevo_diccionario = {nombre: edad for (nombre , edad) in zip(nombres,edades)}
print(nuevo_diccionario)