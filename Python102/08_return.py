
def sum_con_rango(min, max):
    sum = 0
    for x in range (min, max):
        sum+= x
    return(sum)

result = sum_con_rango(1, 100)
print(result)
print(sum_con_rango(1, 100))