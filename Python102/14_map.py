numeros = [1, 2, 3, 4]
numeros_v2 = []
for i in numeros:
    numeros_v2.append(i * 2)

numeros_v3 = list(map(lambda i: i * 2, numeros))

print(numeros)
print(numeros_v2)
print(numeros_v3)

numeros_1 = [1, 2, 3, 4]
numeros_2 = [5, 6, 7, 8]

print(numeros_1)
print(numeros_2)

result = list(map(lambda x,y : x+y, numeros_1,numeros_2))
print(result)