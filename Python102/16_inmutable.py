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

def add_taxes(item):
    nuevo_item = item.copy()
    nuevo_item['taxes'] = nuevo_item['precio'] * .19
    return nuevo_item

new_items = list(map(add_taxes,items))
print('Nueva Lista')
print(new_items)
print('Vieja lista')
print(items)
