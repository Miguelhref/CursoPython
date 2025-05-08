import time
from src.models.Product import Product

class MiraviaProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_telegram_message(self) -> str:
        message = 'El producto <b>{}</b>'.format(self.name)

        if not self.is_new_product:
            if self.percent_of_discount() > 70:
                message = '🔥[{}]🔥 {}'.format(self.format_percent_of_discount(), message)

            message += ' ha bajado de <b>{}</b> a <b>{}</b> ({})'.format(self.format_old_price(), self.format_price(), self.format_percent_of_discount())
        else:
            message += ' ha aparecido nuevo en la keyword <b>{}</b> con el precio de <b>{}</b>'.format(self.keyword, self.format_price())

            if self.pvp != None:
                message += ' que baja desde los <b>{}</b>'.format(self.format_pvp())

        if (self.coupon):
            message += '\nCon cupón de {}: {}'.format(self.format_coupon(), self.format_price_with_coupon())

        message += '\nEnlace: {}'.format(self.url_item)

        return message

export = MiraviaProduct