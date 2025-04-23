items = [

    {
        'producto': 'camisa',
        'precio': 100,
    },
    {
        'producto':'pantalones',
        'precio': 300
    },
    {
        'producto': 'pantalones 2',
        'precio': 200
    }

]

precios = list(map(lambda item: item['precio'], items))
print(precios)

def add_taxes(item):
    item['taxes'] = item['precio'] * .19
    return item

new_items = list(map(add_taxes,items))
print(new_items)