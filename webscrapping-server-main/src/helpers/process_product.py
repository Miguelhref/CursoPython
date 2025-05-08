import time

from src.repository.Product import ProductRepo
from src.repository.WesternDigital import WesternDigitalRepo

def process_product(product_obj, store, keyword = None):
    query_product = ProductRepo.get_by_sku(product_obj.sku, store['id'], 'id, price, pvp, last_price_changed')

    if (query_product == None):
        print('Añadiendo producto')

        product_added = ProductRepo.add(product_obj.to_json())

        if (keyword != None and keyword['alert_new'] != None):
            product_obj.is_new_product = keyword['alert_new']

        product_obj.id = product_added['id']

    else:
        product_obj.id = query_product['id']

        if (query_product['price'] != None):
            query_product['price'] = float(query_product['price'])

        if (query_product['pvp'] != None):
            query_product['pvp'] = float(query_product['pvp'])

        if (product_obj.price == query_product['price']):
            return product_obj

        print('Actualizando producto')

        product_obj.old_price = query_product['price']
        product_obj.last_price_changed = time.time() * 1000

        ProductRepo.update(product_obj.sku, store['id'], product_obj.to_json(), None)
    if (keyword != None):
        product_obj.keyword_id = keyword['id']
        product_obj.keyword = keyword['keyword']
        product_obj.send_to_telegram = store['active'] and keyword['active'] and (product_obj.is_new_product or product_obj.percent_of_discount() >= keyword['porcentage'])
    else:
        product_obj.send_to_telegram = store['active']

    return product_obj

