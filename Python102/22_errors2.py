try:
    #print(0/0)
    assert 1 != 2, 'Uno no es igual que uno'
    edad = 19
    if edad < 18:
     raise Exception('No se permiten menores de 18 años')

except ZeroDivisionError as error:
    print(error)
except AssertionError as error:
    print(error)

print('Hola')