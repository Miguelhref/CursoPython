import time
from src.models.Product import Product

class AmazonReacoProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_seen = kwargs.get('last_seen', 0)

    def create_telegram_message(self) -> str:
        message = ''

        if (self.is_new_product):
            message += '[NUEVO] Se ha detectado un nuevo reacondicionado en keyword {}.\n'.format(self.keyword)
        else:
            message += '[VUELVE] Ha vuelto el stock de este reacondicionado en keyword {}.\n'.format(self.keyword)

        message += 'Nombre: {}'.format(self.name)

        if (self.price > 0):
            message += '\nPrecio Reacon: {}'.format(self.format_price())

        message += '\nEnlace: {}'.format(self.url_item)

        return message

    def is_last_seen_one_week_ago(self):
        if (not self.last_seen):
            return False

        return self.last_seen + 604800000 < time.time() * 1000

export = AmazonReacoProduct