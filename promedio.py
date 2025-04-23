def venta(*args, **kwargs):
    precios = args
    descuento = kwargs

    if descuento:
        total = sum(precios)*(1-(descuento.get("descuento")/100))
        print(f"El total con descuentos es {total}")
       
    else:
        total = sum(precios)
        print(f"El total sin descuentos es {total}")

venta(1000,2000,7000)
venta(1000,2000,7000,descuento=20)

                

        