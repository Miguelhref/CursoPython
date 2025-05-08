import time
from src.models.Product import Product

class PremiumExprimeViajesProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_telegram_message(self) -> str:
        message = 'Nuevo producto en <b>ExprimeViajes Premium</b>.\n\n'
        message += 'Nombre: {}\n'.format(self.name)

        if self.price and self.price > 0:
            message += 'Precio: {}\n'.format(self.format_price())

        message += 'Enlace: {}'.format(self.url_item)

        return message

export = PremiumExprimeViajesProduct