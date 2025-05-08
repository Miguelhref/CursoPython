import time
from src.models.Product import Product

class MiraviaFlashProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_discount = kwargs.get('item_discount')
        self.item_curent_stock = kwargs.get('item_curent_stock')
        self.base_price = kwargs.get('base_price')

    def create_telegram_message(self) -> str:
        message = 'Nombre: {}\nPrecio base: {}\nPrecio oferta: {}\nDescuento: {}\nStock: {}'.format(
            self.name,
            self.format_to_curreny(self.base_price),
            self.format_price(),
            self.item_discount,
            self.item_curent_stock
            )

        message += '\nURL: {}'.format(self.url_item)

        return message

export = MiraviaFlashProduct