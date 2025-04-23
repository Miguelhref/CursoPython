cuadrados = [x**2 for x in range(1,11)]
#print("Cuadrados:", cuadrados)

celsius = [0,10,20,30,40]
fahrenheit = [(temp * 9/5)+32 for temp in celsius]
#print("Temperatura en F:",fahrenheit)


#Numeros pares
pares = [x for x in range (1,21) if x%2 == 0]
#print(pares)

matriz = [[1,2,3],
          [4,5,6],
          [7,8,9]]

transpuesta = [[row[i] for row in matriz] for i in range(len(matriz[0]))]

#print(matriz)
#print(transpuesta)

numeros1 = [1,2,3,4,5]
numeros2 = [x*2 for x in numeros1]
#print(numeros2)

palabras1 = ["sol", "mar", "montaña", "rio", "estrella"]
palabras2 = [palabra.upper() for palabra in palabras1 if len(palabra)>3]
#print (palabras2)

claves = ["nombre", "edad", "ocupación"]
valores = ["Juan", 30, "Ingeniero"]

diccionario = {claves[i]:valores[i] for i in range(len(claves)) }
print(diccionario)
