def find_volume(length=1, width=1, depth=1):
    return length * width * depth, width, 'hola'


result = find_volume(10, 20, 3)
print(result)

result = find_volume()
print(result)

result = find_volume(width=10)
print(result)
result = find_volume(width=10)
print(result[0])
print("-------")
valor_retorno1, valor_retorno2, valor_retorno3 = find_volume(width=10)
print(valor_retorno1)
print(valor_retorno2)
print(valor_retorno3)