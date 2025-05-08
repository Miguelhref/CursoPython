
import json
import locale
import time

# from src.models.Store import Store
# from src.models.Keyword import Keyword

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

class Product:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.sku = kwargs.get('sku')
        self.url_item = kwargs.get('url_item')
        self.url_img = kwargs.get('url_img')
        self.name = kwargs.get('name')
        self.price = kwargs.get('price')
        self.old_price = kwargs.get('old_price')
        self.pvp = kwargs.get('pvp')
        self.last_price_changed = kwargs.get('last_price_changed')
        self.last_notified = kwargs.get('last_notified')
        self.keyword_id = kwargs.get('keyword_id')
        self.keyword = kwargs.get('keyword')
        self.store_id = kwargs.get('store_id')
        self.currency = kwargs.get('currency', '€')
        self.is_new_product = kwargs.get('is_new_product', False)
        self.table_name = kwargs.get('table_name', 'productos')
        #self.coupon = kwargs.get('coupon', None)
        self.send_to_telegram = kwargs.get('send_to_telegram', False)

    def create(self, product):
        return self.add(self.to_json())

    def to_json(self):
        return self.__dict__

    def percent_of_discount(self):
        if (self.old_price == None or self.old_price == 0):
            return 0

        return (self.old_price - self.price) / self.old_price * 100

    def format_price(self) -> str:
        return self.format_to_curreny(self.price)

    def format_old_price(self) -> str:
        return self.format_to_curreny(self.old_price)

    def format_pvp(self) -> str:
        return self.format_to_curreny(self.pvp)

    def format_percent_of_discount(self) -> str:
        return self.format_number(self.percent_of_discount()) + "%"

    def format_to_curreny(self, number) -> str:
        if (self.currency == "£"):
            return self.currency + ' ' + self.format_number(number)

        return self.format_number(number) + " " + self.currency

    def format_number(self, number) -> str:
        if (not number):
            return "0"

        return locale.format_string('%.2f', number, True)

    def format_coupon(self) -> str:
        if (not self.coupon):
            return ''

        return self.format_number(self.coupon['value']) + (" " if self.coupon['type'] == '€' else '') + self.coupon['type']

    def format_price_with_coupon(self):
        if not self.coupon:
            return ''

        if self.coupon['type'] == '%':
            return self.format_to_curreny(self.price - (self.price * (self.coupon['value'] / 100)))

        if self.coupon['type'] == '€':
            return self.format_to_curreny(self.price - self.coupon['value'])

        return ''

    def create_telegram_message(self) -> str:
        message = ''

        message += "El producto <b>{}</b>".format(self.name)

        formated_percent = self.format_percent_of_discount()
        formated_price = self.format_price()
        formated_old_price = self.format_old_price()
        formated_pvp = self.format_pvp()

        if self.is_new_product:
            message += " ha aparecido nuevo en la keyword <b>{}</b> con el precio:\n\n".format(self.keyword)
            message += "▪️ Precio: <b>{}</b>".format(formated_price)
        
            if self.pvp is not None:
                message += "\n▪️ Precio antes: <b>{}</b>".format(formated_pvp)
        else:
            message += " ha bajado de precio:\n\n"
            if self.percent_of_discount() >= 70:
                message = "🔥[{}]🔥 {}".format(formated_percent, message)
                
            message += "▪️ Precio AHORA: <b>{}</b>\n".format(formated_price)
            message += "▪️ Precio antes: <b>{}</b> ({})".format(formated_old_price, formated_percent)

        message += "\n\nEnlace: {}".format(self.url_item)

        return message

export = Product
