precio = 100 #Alcance global

def increment():
    precio = 200
    result = precio + 10
    print(result)
    return result

result  = increment()
print(precio)
precio_2=increment()
print(precio_2) 
print(result)