import time
import re
from fastapi import APIRouter, Body, Depends, Request, Header
from psycopg2.errors import UniqueViolation, UndefinedColumn, UndefinedTable

from src.requests_model.clientGetData import clientGetData
from src.requests_model.clientAddProducts import clientAddProducts
from src.requests_model.clientAddProductsToStore import clientAddProductsToStore
from src.requests_model.clientAddProductsAmazonFlash import clientAddProductsAmazonFlash
from src.requests_model.clientAddProductsWesternDigital import clientAddProductsWesternDigital
from src.requests_model.clientChekProductAmazonReaco import clientChekProductAmazonReaco
from src.requests_model.clientAddProductsMiraviaFlash import clientAddProductsMiraviaFlash
from src.requests_model.clientGetDataAmazonAsin import clientGetDataAmazonAsin
from src.requests_model.clientAddProductsToAmazonAsin import clientAddProductsToAmazonAsin

from src.models.ClientRequest import ClientRequest
from src.models.Product import Product
from src.models.AmazonFlashProduct import AmazonFlashProduct
from src.models.WesternDigitalProduct import WesternDigitalProduct
from src.models.AmazonReacoProduct import AmazonReacoProduct
from src.models.PremiumExprimeViajesProduct import PremiumExprimeViajesProduct
from src.models.MiraviaProduct import MiraviaProduct
from src.models.MiraviaFlashProduct import MiraviaFlashProduct
from src.models.AmazonAsinProduct import AmazonAsinProduct

from src.middlewares.jwt import JWTBearer

from src.helpers.has_blacklist import has_blacklist
from src.helpers.sku_cache import in_cache
from src.helpers.ApiError import ApiError
from src.helpers.process_product import process_product

from src.repository.ScheduledMessages import ScheduledMessagesRepo
from src.repository.Product import ProductRepo
from src.repository.Keyword import KeywordRepo
from src.repository.Store import StoreRepo
from src.repository.Token import TokenRepo
from src.repository.Cache import CacheRepo
from src.repository.WesternDigital import WesternDigitalRepo
from src.repository.AmazonAsins import AmazonAsinsRepo

from message_scheduler import message_scheduler

router = APIRouter()

def update_token_last_seen(token):
    token_split = token.split(" ")
    token = token_split[1] if len(token_split) > 1 else token_split[0]
    TokenRepo.update_last_seen(token, time.time() * 1000)

@router.post("/client/getDataFrom/keywords", dependencies=[Depends(JWTBearer())])
def get_data(body: clientGetData = Body(...)):
    store_name = body.storeName

    if (store_name == None):
        raise ApiError(status=400, ok=False, reason="STORE_NAME_IS_REQUIRED")

    store = StoreRepo.get_by_name(store_name, 'id, active')

    if (store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    if (not store['active']):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_ACTIVE")

    keyword = KeywordRepo.get_by_store_id_first_last_checked(store['id'])

    if (keyword == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

    KeywordRepo.update_last_checked(keyword['id'], time.time() * 1000)

    return { "ok": True, "dataScraper": keyword, "storeId": store['id'] }

@router.post("/client/getDataFrom/noKeywords", dependencies=[Depends(JWTBearer())])
def get_data_no_keywords(body: clientGetData = Body(...)):
    store_name = body.storeName

    if (store_name == None):
        raise ApiError(status=400, ok=False, reason="STORE_NAME_IS_REQUIRED")

    store = StoreRepo.get_by_name(store_name, 'id, active')

    if (store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    if (not store['active']):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_ACTIVE")

    return { "ok": True, "storeId": store['id'] }

@router.post("/client/product/add", dependencies=[Depends(JWTBearer())])
def add_product(request: Request,authorization: str = Header(None), body: clientAddProducts = Body(...)):
    # Obtener la IP del cliente
    #client_ip = request.client.host
    #print(f"Request received from IP: {client_ip}")
    products = body.products
    keyword_id = body.keywordId

    if (keyword_id == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_ID_IS_REQUIRED")

    query_keyword = KeywordRepo.get_by_id(keyword_id, 'id, blacklist, keyword, alert_new, porcentage, active, store_id')
    query_store = StoreRepo.get_by_id(query_keyword['store_id'], 'id, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_keyword['store_id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        if (has_blacklist(product.name, query_keyword['blacklist'])):
            continue

        product_obj = Product(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
        )

        process_product(product_obj, query_store, query_keyword)
        #print("LLEGA AQUI")
        message_scheduler.schedule(product_obj, query_store)
        #print("Paso por aqui")

    KeywordRepo.update_last_checked(query_keyword['id'], time.time() * 1000)

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/product/amazonFlash/add", dependencies=[Depends(JWTBearer())])
def add_product_amazon_flash(authorization: str = Header(None), body: clientAddProductsAmazonFlash = Body(...)):
    products = body.products
    store_id = body.storeId

    query_store = StoreRepo.get_by_id(store_id, 'id, name, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    if (query_store['name'] != 'Amazon_Flash'):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_VALID")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_keyword['store_id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        product_obj = AmazonFlashProduct(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
            coupon = product.coupon,
            promotion_codes = product.promotion_codes,
        )

        process_product(product_obj, query_store)
        message_scheduler.schedule(product_obj, query_store)

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/product/westernDigital/add", dependencies=[Depends(JWTBearer())])
def add_product_western_digital(authorization: str = Header(None), body: clientAddProductsWesternDigital = Body(...)):
    products = body.products
    store_id = body.storeId

    query_store = StoreRepo.get_by_id(store_id, 'id, name, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    if (query_store['name'] != 'western_digital'):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_VALID")

    for product in products:
        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_keyword['store_id'])):
            continue

        if (not product.stockLevel):
            product.stockLevel = 0

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        product_obj = WesternDigitalProduct(
            sku = product.code,
            code = product.code,
            name = product.name,
            price = product.price,
            stock_level = product.stockLevel,
            store_id = query_store['id']
        )

        query_product = WesternDigitalRepo.get_by_code(product_obj.code)
        stock_change = False

        if (query_product == None):
            print('Añadiendo producto')
            product_added = WesternDigitalRepo.add(product_obj.to_json())
            product_obj.id = product_added['id']
        else:
            product_obj.id = query_product['id']

            if (query_product['price'] != None):
                query_product['price'] = float(query_product['price'])

            if (product_obj.price != query_product['price']):
                print('Actualizando producto')
                product_obj.old_price = query_product['price']
                product_obj.last_price_changed = time.time() * 1000

            if (query_product['stock_level'] == None or query_product['stock_level'] == 0) and product_obj.stock_level and product_obj.stock_level != 0:
                print('Actualizando stock')
                stock_change = True

            WesternDigitalRepo.update(product_obj.code, product_obj.to_json(), None)

        discount = product_obj.percent_of_discount()

        if (not (product_obj.stock_level > 0 and (discount >= 10 or stock_change))):
            continue

        product_obj.send_to_telegram = query_store['active']

        if (not message_scheduler.can_schedule(product_obj)):
            continue

        if (discount >= 10):
            message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid'])

        if (stock_change):
            product_obj.stock_change = True
            message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid'])

        if (query_store['tg_chatid_bigdrop'] != None and product_obj.percent_of_discount() >= (query_store['percentage_bigdrop'] if query_store['percentage_bigdrop'] != None else 50)):
            product_obj.stock_change = False
            product_obj.is_big_drop = True
            product_obj.old_price = query_product['price']
            message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid_bigdrop'])

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/product/amazonReaco/add", dependencies=[Depends(JWTBearer())])
def add_product_amazon_reaco(authorization: str = Header(None), body: clientAddProducts = Body(...)):
    products = body.products
    keyword_id = body.keywordId

    if (keyword_id == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_ID_IS_REQUIRED")

    query_keyword = KeywordRepo.get_by_id(keyword_id, 'id, blacklist, keyword, alert_new, porcentage, active, store_id')
    query_store = StoreRepo.get_by_id(query_keyword['store_id'], 'id, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_keyword['store_id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        if (has_blacklist(product.name, query_keyword['blacklist'])):
            continue

        product_obj = AmazonReacoProduct(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
            keyword_id = query_keyword['id'],
            keyword = query_keyword['keyword'],
        )

        query_product = ProductRepo.get_by_sku(product_obj.sku, query_store['id'], 'id, price, pvp, last_price_changed, last_seen')

        if (query_product == None):
            print('Añadiendo producto')

            product_added = ProductRepo.add(product_obj.to_json())
            product_obj.is_new_product = query_keyword['alert_new']
            product_obj.id = product_added['id']
        else:
            product_obj.id = query_product['id']

            if (query_product['price'] != None):
                query_product['price'] = float(query_product['price'])

            if (query_product['pvp'] != None):
                query_product['pvp'] = float(query_product['pvp'])

            if (product_obj.price != query_product['price']):
                print('Actualizando producto')

                product_obj.old_price = query_product['price']
                product_obj.last_price_changed = time.time() * 1000
                ProductRepo.update(product_obj.sku, query_store['id'], product_obj.to_json(), None)

            product_obj.last_seen = query_product['last_seen'] if query_product['last_seen'] != None else 0

        ProductRepo.update_last_seen(product_obj.id, time.time() * 1000)
        product_obj.send_to_telegram = (query_store['active'] and query_keyword['active'] and (product_obj.is_new_product or product_obj.is_last_seen_one_week_ago()))

        if (not message_scheduler.can_schedule(product_obj)):
            continue

        product_obj.last_seen = time.time() * 1000
        message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid'])

    KeywordRepo.update_last_checked(query_keyword['id'], time.time() * 1000)
    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/product/amazonReaco/checkProduct", dependencies=[Depends(JWTBearer())])
def check_product(body: clientChekProductAmazonReaco = Body(...)):
    sku = body.sku
    keyword_id = body.keywordId

    if (keyword_id == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_ID_IS_REQUIRED")

    query_keyword = KeywordRepo.get_by_id(keyword_id, 'alert_new, store_id')
    query_store = StoreRepo.get_by_id(query_keyword['store_id'], 'id')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    product_query = ProductRepo.get_by_sku(sku, query_store['id'], 'last_seen')

    if (product_query == None):
        return { "check": query_keyword['alert_new'] }

    product_obj = AmazonReacoProduct(
        last_seen = product_query['last_seen'] if product_query['last_seen'] != None else 0
    )

    return { "check": product_obj.is_last_seen_one_week_ago() }

@router.post("/client/product/aremiumExprimeViajes/add", dependencies=[Depends(JWTBearer())])
def add_product_aremium_exprime_viajes(authorization: str = Header(None), body: clientAddProductsToStore = Body(...)):
    store_id = body.storeId
    products = body.products

    query_store = StoreRepo.get_by_id(store_id, 'id, name, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_store['id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        product_obj = PremiumExprimeViajesProduct(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
        )

        query_product = ProductRepo.get_by_sku(product_obj.sku, query_store['id'], 'id')

        if (query_product == None):
            print('Añadiendo producto')

            product_added = ProductRepo.add(product_obj.to_json())
            product_obj.id = product_added['id']
        else:
            continue

        message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid'])

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/sendDataTo/miravia", dependencies=[Depends(JWTBearer())])
def send_data_to_miravia(authorization: str = Header(None), body: clientAddProducts = Body(...)):
    products = body.products
    keyword_id = body.keywordId

    if (keyword_id == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_ID_IS_REQUIRED")

    query_keyword = KeywordRepo.get_by_id(keyword_id, 'id, blacklist, keyword, alert_new, porcentage, active, store_id')

    if (query_keyword == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

    query_store = StoreRepo.get_by_id(query_keyword['store_id'], 'id, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_keyword['store_id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        if (has_blacklist(product.name, query_keyword['blacklist'])):
            continue

        product_obj = MiraviaProduct(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
            #coupon = product.coupon,
        )

        process_product(product_obj, query_store, query_keyword)

        if (not message_scheduler.can_schedule(product_obj)):
            continue

        if product_obj.is_new_product:
            message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid'])
        else:
            if (query_store['tg_chatid_bigdrop'] != None):
                message_scheduler.add_to_schedule(product_obj, query_store['tg_chatid_bigdrop'])

    KeywordRepo.update_last_checked(query_keyword['id'], time.time() * 1000)

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/sendDataTo/miraviaFlash", dependencies=[Depends(JWTBearer())])
def send_data_to_miravia(authorization: str = Header(None), body: clientAddProductsMiraviaFlash = Body(...)):
    products = body.products
    store_id = body.storeId

    query_store = StoreRepo.get_by_id(store_id, 'id, name, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')

    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (product.price == None or product.price <= 0):
            continue

        if (in_cache(product.sku + '-' + str(product.price), query_store['id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        product_obj = MiraviaFlashProduct(
            sku = product.sku,
            url_item = product.url_item,
            url_img = product.url_img,
            name = product.name,
            price = product.price,
            pvp = product.pvp,
            store_id = query_store['id'],
            #coupon = product.coupon,
            item_discount = product.itemDiscount,
            item_curent_stock = product.itemCurrentStock,
            base_price = product.base_price
        )

        process_product(product_obj, query_store)
        print(product_obj.name)
        message_scheduler.schedule(product_obj, query_store)

    update_token_last_seen(authorization)

    return { "ok": True }

@router.post("/client/getDataFrom/amazon_asins", dependencies=[Depends(JWTBearer())])
def get_data_from_amazon_asins(authorization: str = Header(None), body: clientGetDataAmazonAsin = Body(...)):
    store_name = body.storeName
    table_name = body.tableName

    try:
        query_store = StoreRepo.get_by_name(store_name, '*')

        if (query_store == None):
            raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

        if (not query_store['active']):
            raise ApiError(status=400, ok=False, reason="STORE_NOT_ACTIVE")

        query_products = AmazonAsinsRepo.get_all_active_by_last_checked(table_name)

        if (query_products == None):
            raise ApiError(status=400, ok=False, reason="NO_PRODUCTS_TO_CHECK")

        for product in query_products:
            AmazonAsinsRepo.update_last_checked(product['asin'], time.time() * 1000, table_name)

        return { "ok": True, 'storeId': query_store['id'], 'productsToScraper': query_products }
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="TABLE_NOT_FOUND")

@router.post('/client/sendDataTo/amazon_asins', dependencies=[Depends(JWTBearer())])
def send_data_to_amazon_asins(authorization: str = Header(None), body: clientAddProductsToAmazonAsin = Body(...)):
    table_name = body.tableName
    currency = body.currency
    products = body.products
    store_id = body.storeId

    query_store = StoreRepo.get_by_id(store_id, 'id, name, tg_chatid, tg_chatid_bigdrop, percentage_bigdrop, active')
    print(f'query_store {query_store}')
    if (query_store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    for product in products:
        if (product.sku == None):
            continue

        if (in_cache(product.sku + '-' + str(product.price_new) + '-' + str(product.price_reaco), query_store['id'])):
            continue

        if (product.url_item == None):
            continue

        if (product.name == None):
            product.name = '-SIN NOMBRE-'

        query_product = None

        try:
            query_product = AmazonAsinsRepo.get_by_asin(product.sku, table_name)
        except UndefinedTable as e:
            raise ApiError(status=400, ok=False, reason="TABLE_NOT_FOUND")

        if (query_product == None):
            continue
        
        product_obj = AmazonAsinProduct(
            id = query_product['id'],
            asin = query_product['asin'],
            url_item = product.url_item,
            name = query_product['name'],
            price_new = product.price_new,
            price_reaco = product.price_reaco,
            pvp = product.pvp,
            store_id = query_store['id'],
            table_name = table_name,
            currency = currency
        )

        if query_product['price_new'] != None:
            query_product['price_new'] = float(query_product['price_new'])
        else:
            query_product['price_new'] = 0.0

        if query_product['price_reaco'] != None:
            query_product['price_reaco'] = float(query_product['price_reaco'])
        else:
            query_product['price_reaco'] = 0.0

        if (query_product['price_reaco_alert'] != None):
            query_product['price_reaco_alert'] = float(query_product['price_reaco_alert'])
        else:
            query_product['price_reaco_alert'] = 0.0

        if (query_product['price_new_alert'] != None):
            query_product['price_new_alert'] = float(query_product['price_new_alert'])
        else:
            query_product['price_new_alert'] = 0.0

        if product_obj.price_new != query_product['price_new'] or product_obj.price_reaco != query_product['price_reaco']:
            product_obj.last_price_changed = time.time() * 1000
            AmazonAsinsRepo.update(product_obj.sku, table_name, product_obj.to_json())

        if not query_store['active']: 
            continue

        query_product['tg_chatid_bigdrop'] = None

        if (product_obj.price_new  != None and product_obj.price_new <= query_product['price_reaco_alert']):
            product_obj.price = product_obj.price_new
            product_obj.old_orice = query_product['price_new']
            product_obj.is_new = True
            product_obj.price_alert = query_product['price_new_alert']
            product_obj.send_to_telegram = True
            message_scheduler.schedule(product_obj, query_store)

        if (product_obj.price_reaco != None and product_obj.price_reaco <= query_product['price_reaco_alert']):
            product_obj.price = product_obj.price_reaco
            product_obj.old_orice = query_product['price_reaco']
            product_obj.is_new = False
            product_obj.is_reaco = True
            product_obj.price_alert = query_product['price_reaco_alert']
            product_obj.send_to_telegram = True
            message_scheduler.schedule(product_obj, query_store)

        AmazonAsinsRepo.update_last_checked(product_obj.sku, time.time() * 1000, table_name)

    update_token_last_seen(authorization)


export = router