import time
from src.models.Product import Product

class AmazonAsinProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.asin = kwargs.get('asin', None)
        self.sku = self.asin
        self.price_new = kwargs.get('price_new', None)
        self.price_reaco = kwargs.get('price_reaco', None)
        self.is_reaco = kwargs.get('is_reaco', False)
        self.is_new = kwargs.get('is_new', False)
        self.price_alert = kwargs.get('price_alert', None)
        self.table_name = kwargs.get('table_name', 'productos_amazon_asin')


    def create_telegram_message(self) -> str:
        message = 'El producto <b>{}</b>'.format(self.name)

        price = self.format_to_curreny(self.price_new) if self.is_new else self.format_to_curreny(self.price_reaco) if self.is_reaco else -1
        post_type = "nuevo" if self.is_new else "reaco"

        message += ' ha alcanzado el precio deseado {} <b>{}</b> al que baja (Alerta establecida: <b>{}</b>)'.format(post_type, price, self.format_to_curreny(self.price_alert))
        message += '\nEnlace: {}'.format(self.url_item)

        return message

export = AmazonAsinProduct