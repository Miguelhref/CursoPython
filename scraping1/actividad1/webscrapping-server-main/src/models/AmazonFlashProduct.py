from src.models.Product import Product

class AmazonFlashProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_codes = kwargs.get('promotion_codes', [])

    def create_telegram_message(self) -> str:
        message = '[NUEVO FLASH]\nNombre: {}\nPrecio: {}'.format(self.name, self.format_price())

        if (self.coupon):
            message += '\nCupón: {}'.format(self.format_coupon())

        if (len(self.promotion_codes) > 0):
            message += '\nCódigos: {}'.format(', '.join(map(lambda code: code['code'], self.promotion_codes)))

        message += '\nURL: {}'.format(self.url_item)

        return message