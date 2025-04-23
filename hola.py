numbers = {1:"uno", 2:"dos",3:"tres"}
print(numbers)
print(numbers[1])
information = {"nombre":"Paco",
               "apellido":"Lopez",
               "altura":1.75,
               "edad":58}

print (information)

del(information["altura"])
print(information)
print (information.keys())
claves = information.keys()
print(claves)
print(information.items())

information2 = {"Paco":{"Nombre":"Paco",
                        "Apellido":"Lopez"},
                "Manolo":{"Nombre":"Manolo",
                          "Apellido":"Perez"}}
print(information2["Paco"])