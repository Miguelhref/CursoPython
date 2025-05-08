from src.models.Product import Product

class WesternDigitalProduct(Product):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get('code', None)
        self.stock_level = kwargs.get('stock_level', None)
        self.url_item = "https://shop.westerndigital.com/es-es/search?q=__PRODUCT_CODE__"
        self.stock_change = False
        self.is_big_drop = False

    def create_telegram_message(self) -> str:
        url = self.url_item.replace("__PRODUCT_CODE__", self.code)

        if (self.stock_change):
            return """
            ✅ Entrada en Stock para producto agotado.\n🙊 Requiere revisión manual \nNombre: {}\nPrecio: {}\nStock: {}\n{}
            """.format(self.name, self.format_price(), self.stock_level, url)

        if (self.is_big_drop):
            return """
            🔥[{}]🔥 🙈 Bajada tocha detectada en Western Digital 🐒.\nNombre: {}\nPrecio: {} -> {} ({})\nStock: {}\n{}
            """.format(self.format_percent_of_discount(), self.name, self.format_old_price(), self.format_price(), self.format_percent_of_discount(), self.stock_level, url)

        return """
        🙈 Bajada detectada en Western Digital 🐒.\nNombre: {}\nPrecio: {} -> {} ({})\nStock: {}\n{}
        """.format(self.name, self.format_old_price(), self.format_price(), self.format_percent_of_discount(), self.stock_level, url)