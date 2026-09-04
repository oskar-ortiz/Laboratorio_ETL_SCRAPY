import scrapy


class SapiensSpider(scrapy.Spider):
    name = "sapiens"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    ]

    def parse(self, response):
        yield {
            "nombre": response.css("div.product_main h1::text").get(default="").strip(),
            "precio": response.css("div.product_main p.price_color::text").get(default="").strip(),
            "disponibilidad": response.css("div.product_main p.instock::text").getall()[-1].strip(),
            "calificacion": response.css("div.product_main p.star-rating::attr(class)").get(default="").replace("star-rating", "").strip(),
        }
