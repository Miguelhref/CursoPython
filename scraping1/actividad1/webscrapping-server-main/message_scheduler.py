import re
import requests
import os
import time
from dotenv import load_dotenv
import random
from apscheduler.schedulers.background import BackgroundScheduler

from src.repository.ScheduledMessages import ScheduledMessagesRepo
from src.repository.Product import ProductRepo
from src.repository.WesternDigital import WesternDigitalRepo
from src.repository.AmazonAsins import AmazonAsinsRepo
from src.repository.Keyword import KeywordRepo
from src.repository.Store import StoreRepo
from src.repository.Cache import CacheRepo

load_dotenv()


class MessageScheduler:
    scheds = dict()
    def __init__(self):
        self.tokens = [os.getenv("BOT_API"),os.getenv("BOT_API_2"),os.getenv("BOT_API_3"),os.getenv("BOT_API_4"),os.getenv("BOT_API_5"),os.getenv("BOT_API_6")]
        self.general_chat_id = os.getenv('GENERAL_TG_CHATID')
        #self.chat_id = os.getenv("CHAT_ID_TELEGRAM")
    def get_random_token(self):
        return random.choice(self.tokens)
    def send_to_pushover(self, message):
        url = "https://api.pushover.net/1/messages.json"
        user_keys = [os.getenv('USER_KEY_PUSHOVER'), os.getenv('USER_KEY_PUSHOVER_2')]
        app_token = os.getenv('APP_TOKEN_PUSHOVER')
        print(f"USER_KEY_PUSHOVER: {user_keys}")
        print(f"APP_TOKEN_PUSHOVER: {app_token}")
        print(f"Mensaje a enviar: {message}")

        for user_key in user_keys:
            if not user_key:
                print("Clave de usuario vacía, se omite.")
                continue

            data = {
                "token": app_token,
                "user": user_key,
                "message": message
            }

            try:
                response = requests.post(url, data=data, timeout=30)
                response.raise_for_status()
                if response.status_code == 200:
                    print(f'Push enviado exitosamente a {user_key}!', response.text)
                else:
                    print(f'Error al enviar push a {user_key}:', response.text)
            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud para {user_key}: {e}")


    def send_to_telegram(self, message, chat_id):
        token = self.get_random_token()
        #print(f"BOT_TOKEN: {token}")
        api_url = f'https://api.telegram.org/bot{token}/sendMessage'
        #print(f'Enviando mensaje a telegram al chatid {chat_id}')
        response = requests.post(api_url, json={ 'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML' }, timeout=30)
        #print(message,"MENSAJE")
        try:
            response.raise_for_status()  
            if response.status_code == 200:
                print('Message sent successfully!', response.text)
                print(response.status_code)
            else:
                print('Failed to send message:', response.text)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        print('-'*40)
        contiene_portatil = re.search(r'\bport[aá]til\b', message, re.IGNORECASE)
        match = re.search(r'descuento\s:\s(\d{1,3}(?:[.,]\d+)?)%', message, flags=re.IGNORECASE)
        if match:
            porcentaje = float(match.group(1).replace(',', '.'))
            print(f'Porcentaje: {porcentaje}')
        else:
            print('No se encontró un porcentaje')
        if contiene_portatil and porcentaje >= 50.0 or porcentaje >= 85.0:
            self.send_to_pushover(message)
            
    def add_sched(self, tg_chatid):

        if tg_chatid in self.scheds:
            return False

        self.scheds[tg_chatid] = BackgroundScheduler()

        self.scheds[tg_chatid].add_job(self.job_messages_scheduler, 'interval', args=[tg_chatid], seconds=3)

        self.scheds[tg_chatid].start()
        return True
#Metodo para quitar el trabajo programado
    def remove_sched(self, tg_chatid):
        if tg_chatid not in self.scheds:
            return False

        self.scheds[tg_chatid].shutdown()
        del self.scheds[tg_chatid]

        return True

    def initialize_scheduler(self):

        keys = list(self.scheds.keys())

        for scheds in keys:
            self.remove_sched(scheds)

        stores = StoreRepo.list('tg_chatid, tg_chatid_bigdrop')

        for store in stores:

            if store['tg_chatid'] != None:
                self.add_sched(store['tg_chatid'])

            if store['tg_chatid_bigdrop'] != None:
                self.add_sched(store['tg_chatid_bigdrop'])
                # AÑADI esto
                self.add_sched(self.general_chat_id)

    # Metodo para programar el mensaje donde recibe el chat_id del bot de telegram
    def job_messages_scheduler(self, tg_chatid):
        message = ScheduledMessagesRepo.get_first(tg_chatid)

        if (message == None):
            return
        # 
        try:

            keyword_query = KeywordRepo.get_by_id(message['keyword_id'], 'active') if message['keyword_id'] != None else None
            store_query = StoreRepo.get_by_id(message['store_id'], 'name, active')

            if (store_query['active'] and (keyword_query == None or keyword_query['active'])):
                self.send_to_telegram(message['message'], message['tg_chatid'])

                if (store_query['name'].lower().find('amazon_asins_') != -1):
                    AmazonAsinsRepo.update_last_notified(message['product_id'], time.time() * 1000, store_query['name'].lower())
                else:
                    if (store_query['name'] != 'western_digital'):
                        ProductRepo.update_last_notified(message['product_id'], time.time() * 1000)
        except Exception as e:
            print(e)

        ScheduledMessagesRepo.delete(message['id'])
    # Metodo para gestionar el almacenamiento del cache de la informacion de los productos
    def process_cache(self, product):

        now = time.time() * 1000

        query_cache = CacheRepo.get_by_sku_and_price(product.sku, product.price, product.store_id, 'id, price, old_price, timestamp')

        if (query_cache == None):
            print('Añadiendo cache')
            query_cache = CacheRepo.add({
                "sku": product.sku,
                "price": product.price,
                "old_price": product.old_price,
                "store_id": product.store_id,
            })
        else:

            if (product.old_price != None and query_cache['old_price'] != product.old_price):
                print('Actualizando old_price cache')

                CacheRepo.update_old_price(query_cache['id'], product.old_price)
        return query_cache
    # Metodo para mirar si se puede programar un mensaje relacionado con el producto en función de su configuración y del tiempo transcurrido desde la última notificación
    def can_schedule(self, product, miliseconds = None):

        if (not product.send_to_telegram):
            return False

        now = time.time() * 1000

        cache = self.process_cache(product)

        if (cache['timestamp'] == None or cache['timestamp'] + (miliseconds if miliseconds != None else 86400000) < now):

            CacheRepo.update_timestamp(cache['id'], now)

            return True

        return False
    # Funcion donde vamos a programar el envio de una notificacion sobre el producto
    def add_to_schedule(self, product, tg_chatid):
        print('Enviando notificación de producto')
        # CAMBIO AQUI
        print(f'Agregando mensaje para el chat_id: {tg_chatid}')
        ScheduledMessagesRepo.add({
            'message': product.create_telegram_message(),
            'tg_chatid': tg_chatid,
            'product_id': product.id,
            'store_id': product.store_id,
            'keyword_id': product.keyword_id
        })

    def schedule(self, product, store, miliseconds = None):

        if (not self.can_schedule(product, miliseconds)):
            return False

        print(store['tg_chatid'])
        print(product)

        self.add_to_schedule(product, store['tg_chatid'])

        if (store['tg_chatid_bigdrop'] != None and product.percent_of_discount() >= (store['percentage_bigdrop'] if store['percentage_bigdrop'] != None else 50)):

            self.add_to_schedule(product, store['tg_chatid_bigdrop'])
            # CAMBIO AQUI
            print(f'Agregando para el canal de BIG DROPS General {self.general_chat_id}')
            self.add_to_schedule(product, self.general_chat_id)


message_scheduler = MessageScheduler()

# resource_id = 1
# frequency = 1

# sched = BackgroundScheduler()

# sched.add_job(initialize_scheduler, 'interval', args=[resource_id, frequency], seconds=1)

# sched.start()
