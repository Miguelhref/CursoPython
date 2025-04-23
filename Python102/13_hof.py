def increment(x):
    return x + 1

increment_v2 = lambda x: x + 1




def high_order_function(x, funcion):
    return x + funcion(x)

high_order_function_v2 = lambda x,funcion : x+funcion(x)

result = high_order_function(2,increment)
print(result)

result2 = high_order_function_v2(2, increment_v2)
print (result2)