import functools

numeros = [1, 2, 3 ,4]

def acum(contador, item):
    print('Contador=> ',contador)
    print('Item=> ',item)
    return contador + item

result = functools.reduce(acum,numeros)
#result = functools.reduce(lambda contador, item:contador + item, numeros)
print(result)
